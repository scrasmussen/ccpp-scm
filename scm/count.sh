#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <bash_output_file>"
    exit 1
fi

input="${1}.cp"
column_1_width=4
column_2_width=53
total_width=$((column_1_width + column_2_width + 7))

count_warning() {
    local warning="$1"
    local count=$(grep -c "${warning}" ${input})
    printf "| %-${column_1_width}s | %-${column_2_width}s |\n" "${count}" "${warning}"
    sed -i "/${warning}/d" ${input}
}
print_line() {
    for ((i=0; i<${total_width}; i++)); do printf '-'; done
    printf '\n'
}


# copy original file
cp ${1} ${input}

print_line
printf "| %-${column_1_width}s | %-${column_2_width}s |\n" "$(grep -c "Warning:" ${input})" "Total Warnings with GNU -Wall"    
print_line
count_warning "Warning: Unused dummy argument"
count_warning "Warning: Unused variable"
count_warning "Warning: Return value"
count_warning "may shadow the intrinsic"
count_warning "Warning: Intrinsic"
count_warning "Warning: Possible change of value"
count_warning "Warning: Nonconforming tab character"
count_warning "Warning: CHARACTER expression will be truncated"
count_warning "Warning: Label"
count_warning "Warning: Unused module variable"
count_warning "may be used uninitialized"
count_warning "Warning: Dummy argument"
count_warning "Warning: Missing '&' in continued character constant"
count_warning "is a dummy argument of the BIND(C) procedure"
count_warning "Warning: Unused PRIVATE module variable" # 
count_warning "Warning: Change of value in conversion"
count_warning "Warning: Type mismatch between actual argument"
count_warning "defined but not used [/-Wunused-function]"
count_warning "Warning: Legacy Extension: REAL array index"
count_warning "Warning: \"CCPP\" redefined"
count_warning "Warning: Line truncated at"
count_warning "Warning: Pointer at"
count_warning "Wcharacter-truncation"
count_warning "Warning: Deleted feature: Start expression in DO loop" # must be integer
count_warning "Wzerotrip" # DO loop will be executed zero times
count_warning "Warning: Same actual argument associated with"
print_line
printf "| %-${column_1_width}s | %-${column_2_width}s |\n" "$(grep -c 'Warning' ${input})" "Unclassified warnings"    
print_line
