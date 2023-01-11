from util.input_parsing import parse_input
from util.snafu import snafu_base10, base10_snafu

print("\nsnafu to base10 examples:")

for number, expected_result in zip(parse_input(example=True,test_case='snafu'),parse_input(example=True,test_case='base10',function=lambda x:int(x))):
    result = snafu_base10(number)
    print(f"\t{number} should equal {expected_result}: result {result} is {'correct' if result == expected_result else 'incorrect'}.")

print("\nBase10 to snafu examples:")   
for number, expected_result in zip(parse_input(example=True,test_case='base10',function=lambda x:int(x)),parse_input(example=True,test_case='snafu')):
    print(f"\n\t Converting {number}")
    result = base10_snafu(number)
    print(f"\t{number} should equal {expected_result}: result {result} is {'correct' if result == expected_result else 'incorrect'}.")
    
example = sum([snafu_base10(number) for number in parse_input(example=True)])
print(f"\nExample input should equal 4890 is base 10 or '2=-1=0' in snafu, result is {example} in base 10 or {base10_snafu(example)} in snafu")

part1 = sum([snafu_base10(number) for number in parse_input(example=False)])
print(f"\nPart 1 output is {part1} in base 10 or {base10_snafu(part1)} in snafu")