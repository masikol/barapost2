### 15.03.2025
masikol:

#### test/test_filesystem.py

1. ##### remove_file_extension
test_remove_file_extension_normal

test_remove_file_extension_multiple_dots

test_remove_file_extension_no_extension

test_remove_file_extension_trailing_dot

test_remove_file_extension_hidden_file

#####  all 5 passed

2. ##### gzip_file

test_gzip_file_normal

test_gzip_file_empty

test_gzip_file_overwrite

#####  all 3 passed

3. ##### empty_dir

test_empty_dir_already_empty

test_empty_dir_with_files

test_empty_dir_with_subdirectories

test_empty_dir_nonexistent

#####  all 4 passed


### 15.03.2025
masikol:

#### test/test_containers/test_fastq.py

1. ##### get_average_quality

test_get_average_quality_uniform

test_get_average_quality_non_uniform

-- test_get_average_quality_caching

#####  all 3 passed

2. ##### test_Q_to_pe

test_Q_to_pe

##### 1 test passed

3. ##### pe_to_Q

test_pe_to_Q

test_pe_to_Q_invalid_zero

test_pe_to_Q_invalid_negative

##### all 3 passed

4. make_quality_dict

test_make_quality_dict_with_fastq

test_make_quality_dict_with_dummy_records

test_make_quality_dict_empty

##### all 3 passed
