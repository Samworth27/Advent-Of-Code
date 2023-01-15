for i in {1..25}; do printf -v name "day%02d" "$i"; mkdir "$name";mkdir "$name/test_cases";mkdir "$name/util" ; done
