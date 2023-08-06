#!/usr/bin/env sh
# -*- coding: utf-8; mode: shell-script; -*-
#
# Copyright 2021 Pradyumna Paranjape
# This file is part of pyprojstencil.
#
# pyprojstencil is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyprojstencil is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyprojstencil.  If not, see <https://www.gnu.org/licenses/>.
#

# Always run this script from its immediate parent folder


set_vars () {
    usage="usage: $0 [-h] [--help]"
    cwd="${PWD}"
    realenv=
    mk_flags=""
    project_root="$(dirname "$(dirname "$(realpath "${0}")")")"
    project_name="$(basename "${project_root}")"
    help_msg="

    DESCRIPTION: Run `make` in ${project_root}/docs folder

    Optional Arguments
    -h:\t\t\tshow usage command line and exit
    --help:\t\tshow this detailed help message and exit
    -r|--realenv:\tforce-override virtualenv check

    Positional Arguments
    All are passed \033[1mverbatim\033[m to make
"
}

unset_vars () {
    cd "${cwd}" || exit 5
    unset usage
    unset help_msg
    unset cwd
    unset realenv
    unset mk_flags
    unset project_root
    unset project_name
}

clean_exit () {
    unset_vars
    if [ -z "${1}" ]; then
        exit 0
    else
        exit "${1}"
    fi
}

cli() {
    while test $# -gt 0; do
        case "${1}" in
            -h)
                printf "%s\n" "${usage}"
                clean_exit 0
                ;;
            --help)
                printf "%s\n" "${usage}"
                # shellcheck disable=SC2059
                printf "${help_msg}\n"
                clean_exit 0
                ;;
            -r|--realenv)
                realenv=true
                shift
                ;;
            *)
                if [ -z "${mk_flags}" ]; then
                    mk_flags="${1}"
                else
                    mk_flags="${mk_flags} ${1}"
                fi
                shift
                ;;
        esac
    done
}

check_venv() {
    if [ -z "${VIRTUAL_ENV}" ] && [ ! ${realenv} ]; then
        printf "\033[1;31m[ERROR]\033[m Not working in a virtualenv\n\n" >&2
        printf "    \033[32m[Recommended]\033[m " >&2
        echo "activate virtualenv by typing without '# ':" >&2
        printf "        # \033[97msource " >&2
        printf "%s/.venv/bin/activate\033[m\n\n" "${project_root}">&2
        printf "    \033[31m[Risky]\033[m " >&2
        printf "else, use --realenv flag to override this error\n" >&2
        printf "        \033[33mDo this only if " >&2
        printf "you understand virtualenv\033[m\n\n" >&2
        echo "Aborting..."
        exit 1
    fi
}

make_docs () {
    pip install -U -r requirements.txt
    make html
    }

main () {
    set_vars "$*"
    cli "$*"
    check_venv
    cd "${project_root}/docs" || exit 5
    make_docs
    clean_exit
}

main "$*"
