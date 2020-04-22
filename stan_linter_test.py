from stan_linter import *

def test_comma():
  line = "y[i] ~ normal(alpha_hat + beta_hat * x[i],sigma_hat);"
  assert(white_space_comma(line) == 
  "missing space after char 42','")

def test_length():
  line = "y[i] ~ normal(alpha_hat + beta_hat * x[i],sigma_hat);" + "y[i] ~ normal(alpha_hat + beta_hat * x[i],sigma_hat);"
  assert(length_gt_80(line) == "line too long at 106 chars, max 80")  

def test_length2():
  line = "y[i] ~ normal(alpha_hat + beta_hat * x[i],sigma_hat);" + "y[i] ~ normal(alpha_hat + beta_hat * x[i],sigma_hat);"
  assert(length_gt_65(line) == "line too long at 106 chars, max 65 for manual")  
  
def test_file_extension():
  line = "foo.stann"
  assert(wrong_suffix(line) == "file name does not end in .stan")
  
def test_lower_case_variables():
  assert(lower_case_variables("real N;") == 
  "Uppercase should only be used as loop constants to allow lower case index variable to match, e.g., for (m in 1:M)")
  assert(lower_case_variables("int N;") == None)
  
def test_open_bracket():
  assert(open_bracket_on_own_line(" { \r\n") == "Open bracket '{' not allowed on own line")
  assert(open_bracket_on_own_line("if() {") == None)
  
def test_multiple_statements():
  assert(multiple_statements_on_line("blah; blah;") == "One statement per line")
  
def test_no_tabs():
  assert(no_tabs("adsf\tadsf") == "Tabs not allowed")
  assert(no_tabs("adsf adsf") == None)
  
def test_indent_spacing():
  assert(two_or_four_indent_spaces("   ") == "indents should be two or four spaces, seeing 3 spaces")
  assert(two_or_four_indent_spaces("  ") == None)
  assert(two_or_four_indent_spaces("\n") == None)

def test_if_else_when_for_space():
  assert if_else_when_for_space("  if(  ")  == "'if(' should have space following if, e.g. 'if ('"
  assert if_else_when_for_space('  for (n in 1:N)') == None

def test_function_call_space():
  assert function_call_space("foo ()") == "'foo ()' has space between function call and ( 'foo()'"
  assert function_call_space('  for (n in 1:N)') == None

def test_space_around_operators():
  assert(space_around_operators("3*4") == "spaces needed around operator *")
  assert(space_around_operators("3 *4") == "spaces needed around operator *")
  assert(space_around_operators("3* 4") == "spaces needed around operator *")
  assert(space_around_operators("3 * 4") == None)
  assert space_around_operators("int<lower = 0> N;") == None
  assert space_around_operators("real<lower=0> sigma;") == "spaces needed around operator ="
  
def test_space_after_prefix_operator():
  assert(space_after_prefix_operator("! foo") == "remove space after operator !")
  assert(space_after_prefix_operator("!foo") == None)
  assert space_after_prefix_operator("alpha + beta") == None
  
def test_space_before_postfix_operator():
  assert(space_before_postfix_operator("foo '") == "remove space before operator '")
  assert(space_before_postfix_operator("foo'") == None)
  
def test_space_after_comma():
  assert(space_after_comma("foo(a,b)") == "add space after comma in function call (a,b")
  assert(space_after_comma("foo(a, b)") == None)

def test_comments():
  assert(comment_block_start("/*") == True)
  assert(comment_block_end("*/") == True)
  assert(line_comment("//") == True)
  assert(line_comment_depreciated("#") == True)
  
def test_windows_cr_lf():
  assert(windows_cr_lf("line of text \r\n") == True)
  assert(windows_cr_lf("line of text \n") == False)

# end to end tests (e2e)
def test_output_e2e(capsys,tmpdir):  
  outfile = tmpdir.mkdir("sub").join("infix.stan")
  with open(outfile,'w') as f:
    f.write("a*b")
  lint_file(outfile)
  captured = capsys.readouterr()
  assert captured.out.rstrip() == "spaces needed around operator *:line number:1='a*b'"
  
def test_windows_cr_lf_e2e(capsys,tmpdir):  
  outfile = tmpdir.mkdir("sub").join("lf_cr.stan")
  with open(outfile,'w') as f:
    f.write('data {\r')
  lint_file(outfile)
  captured = capsys.readouterr()
  assert captured.out.rstrip() == (r"Line contains Widows line termination'\r\n', "
                                   r"please change to unix style '\n':line number:1='data {'")

