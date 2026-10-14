#!/usr/bin/env bash
# Build and run the genomic simulator.
#
#   ./run.sh            live window
#   ./run.sh record N   headless, N frames to out/world.gif
#   ./run.sh bench      headless throughput and population genetics
#   ./run.sh test       every self-checking test, plus a thread-count
#                       determinism check
#   ./run.sh validate   genetic engine against population-genetic theory
#   ./run.sh export     run 3000 ticks, write a VCF sample to out/
#   ./run.sh life       the life world, full screen (Tab picks the world)
#   ./run.sh life-bench headless life world: population, body plans
#                       (GW_PRESET, GW_MODE, GW_DIMS, GW_TICKS, GW_PROFILE)
#   ./run.sh life-video N  N frames rendered headless, to out/life.mp4
#   ./run.sh shot       headless life world renders to out/ (see
#                       life_shot.flow for the GW_ settings)
#   ./run.sh equilibrium  calibrate, solve the attractors, compare cold and
#                       warm starts
#
# OpenMP: Apple clang only links it when libomp's headers and library are on
# the search paths. Without libomp the parallel loops compile serial and the
# results are identical, only slower.
set -euo pipefail
cd "$(dirname "$0")"

for omp in /opt/homebrew/opt/libomp /usr/local/opt/libomp; do
    if [ -d "$omp" ]; then
        export CPATH="$omp/include${CPATH:+:$CPATH}"
        export LIBRARY_PATH="$omp/lib${LIBRARY_PATH:+:$LIBRARY_PATH}"
        break
    fi
done
export FLOW_OPT_LEVEL="${FLOW_OPT_LEVEL:-3}"

quiet() { grep -v -E "ensure_flowc|ℹ️|✅|^-{10,}|Program finished|^Exit code" || true; }

case "${1:-gfx}" in
    gfx)
        flow gfx genomic_world.flow
        ;;
    record)
        mkdir -p out
        flow record genomic_world.flow --frames "${2:-300}" --stride "${3:-1}" \
            --out out/frames --gif out/world.gif
        ;;
    bench)
        flow run bench.flow 2>&1 | quiet
        ;;
    test)
        fail=0
        for t in tests/test_*.flow; do
            echo "== $t"
            if ! (cd tests && flow run "$(basename "$t")") 2>&1 | quiet; then
                fail=1
            fi
            # flow run prints the program's exit code; a nonzero one fails.
        done
        echo "== determinism across thread counts"
        h1=$(cd tests && OMP_NUM_THREADS=1 flow run determinism.flow 2>&1 | grep "^hash" || true)
        h8=$(cd tests && OMP_NUM_THREADS=8 flow run determinism.flow 2>&1 | grep "^hash" || true)
        echo "  1 thread : $h1"
        echo "  8 threads: $h8"
        if [ -z "$h1" ] || [ "$h1" != "$h8" ]; then
            echo "FAIL: state differs between thread counts"
            fail=1
        fi
        echo "== life world determinism across thread counts"
        l1=$(cd tests && OMP_NUM_THREADS=1 flow run life_determinism.flow 2>&1 | grep "^hash" || true)
        l8=$(cd tests && OMP_NUM_THREADS=8 flow run life_determinism.flow 2>&1 | grep "^hash" || true)
        echo "  1 thread : $l1"
        echo "  8 threads: $l8"
        if [ -z "$l1" ] || [ "$l1" != "$l8" ]; then
            echo "FAIL: life world differs between thread counts"
            fail=1
        fi
        echo "== validation against theory"
        mkdir -p out
        if ! flow run validate.flow 2>&1 | quiet; then
            fail=1
        fi
        exit $fail
        ;;
    validate)
        mkdir -p out
        flow run validate.flow 2>&1 | quiet
        ;;
    life)
        flow gfx life_world.flow
        ;;
    shot)
        mkdir -p out
        FLOW_LDFLAGS="-framework CoreText -framework CoreGraphics -framework CoreFoundation" \
            flow run life_shot.flow 2>&1 | quiet
        ;;
    life-bench)
        flow run life_bench.flow 2>&1 | quiet
        ;;
    life-video)
        mkdir -p out/frames
        rm -f out/frames/f_*.ppm
        GW_FRAMES="${2:-300}" GW_OUT=out/frames/f \
        FLOW_LDFLAGS="-framework CoreText -framework CoreGraphics -framework CoreFoundation" \
            flow run life_shot.flow 2>&1 | quiet
        ffmpeg -y -loglevel error -framerate 30 -i out/frames/f_%04d.ppm \
            -c:v libx264 -pix_fmt yuv420p -crf 20 out/life.mp4
        echo "out/life.mp4"
        ;;
    equilibrium)
        mkdir -p out
        flow run equilibrium.flow 2>&1 | quiet
        ;;
    export)
        mkdir -p out
        flow run export_run.flow 2>&1 | quiet
        ;;
    *)
        echo "usage: $0 [gfx|record N [stride]|bench|test|validate|export|equilibrium|life|life-bench|life-video N|shot]" >&2
        exit 2
        ;;
esac
