#!/bin/bash

# Function to display help message
print_help() {
    echo "get_tempo_data.sh: contrib/get_tempo_data.sh [-v,--verbose]"
    echo "    Script for downloading/extracting the TEMPO lookup tables."
    echo ""
    echo "Options:"
    echo "    -v, --verbose    Turn on wget verbose output."
    echo "    --help           Show this help message and exit."
}

verbose="-q"
# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --help)
            print_help
            exit 0
            ;;
        -v|--verbose)
            verbose="-v"
            ;;
        *)
            echo "Unknown option: $1"
            print_help
            exit 1
            ;;
    esac
    shift
done

set -ex

if [[ $(uname -s) == Darwin ]]; then
  if [[ $(sw_vers -productVersion) < 12.3 ]]; then
    MYDIR=$(cd "$(dirname "$(greadlink -f -n "${BASH_SOURCE[0]}" )" )" && pwd -P)
  else
    MYDIR=$(cd "$(dirname "$(readlink -f -n "${BASH_SOURCE[0]}" )" )" && pwd -P)
  fi
else
  MYDIR=$(cd "$(dirname "$(readlink -f -n "${BASH_SOURCE[0]}" )" )" && pwd -P)
fi
BASEDIR=$MYDIR/..

# Change to directory containing the physics input data, download and extract archive
mkdir -p $BASEDIR/scm/data/physics_input_data/
cd $BASEDIR/scm/data/physics_input_data/
wget ${verbose} https://github.com/NCAR/ccpp-scm/releases/download/v7.0.0/tempo_data.tar.gz
tar -xvzf tempo_data.tar.gz
rm -f tempo_data.tar.gz

# The archive uses legacy MP_TEMPO_*.dat names; tempo_v3's Fortran source
# (module_mp_tempo_cfgs.F90) hardcodes different filenames with no
# host/namelist override, so symlink to what it actually looks for.
#
# qr_acr_qg_data_tempo_v3 -> HAILAWARE variant: workaround for an upstream
# bug (see claude_bug_report.md) where initialize_arrays_qr_acr_qg() always
# allocates the hail-aware-sized (nrhg=9) table regardless of hailaware_flag.
ln -sf MP_TEMPO_HAILAWARE_QRacrQG.dat qr_acr_qg_data_tempo_v3
ln -sf MP_TEMPO_QRacrQS.dat           qr_acr_qs_data_tempo_v3
ln -sf MP_TEMPO_freezeH2O.dat         freeze_water_data_tempo_v3

# ccn_activate.bin isn't in the downloaded archive at all -- it's small
# (~35KB) and checked directly into the TEMPO submodule, so symlink it in
# from there instead.
ln -sf $BASEDIR/ccpp/physics/physics/MP/TEMPO/tempo_v3/tables/ccn_activate.bin ccn_activate.bin

cd $BASEDIR/
