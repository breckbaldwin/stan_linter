import io
import re
import sys

def white_space_comma(line):
  result = re.match("(.*,)[^ ].*", line)
  if (result != None):
    prefix_length = len(result.group(1))
    return("missing space after char {}','".format(prefix_length))
  return None
  
def length_gt_80 (line):
  if (len(line) > 80):
    return("line too long at {} chars, max 80".format(len(line)))
  return None

def length_gt_65 (line):
  if (len(line) > 65):
    return("line too long at {} chars, max 65 for manual".format(len(line)))
  return None
  
def wrong_suffix (line):
  if (not line.endswith('.stan')):
    return("file name does not end in .stan")

#see Variable Naming in Stan User's Guide, 
#upper case single letter N allowed for size constants
def lower_case_variables(line):
  variable_name = "\\s*([a-zA-Z0-9_]+)\\s*"
  simple_type = "real|int"
  complex_type1 = "cholesky_factor_corr|corr_matrix|cov_matrix|matrix|row_vector"
  complex_type2 = "positive_ordered|ordered|unit_vector|simplex|vector"
  all_types = "(" + simple_type + "|" + complex_type1 + "|" + complex_type2 + ")"
  result = re.match("\\s*" + all_types + ".*[\\s>\\]]+" + variable_name,line)
  if (result != None):
    type = result.group(1)
    variable = result.group(2)
    if (not re.search("[A-Z]",variable)):
      return None
    elif (type != "int" or len(variable)>1): 
      return "Uppercase should only be used as loop constants to allow lower case index variable to match, e.g., for (m in 1:M)"
  return None

def open_bracket_on_own_line(line):
  if (re.match("^\\s*{\\s*$",line) != None):
    return "Open bracket '{' not allowed on own line"
  return None
  
def multiple_statements_on_line(line):
  if (re.match(".*;.*;",line)):
    return "One statement per line"
  return None

def no_tabs(line):
  if (re.search("\\t",line)):
    return "Tabs not allowed"
  return None

#should be document level 
def two_or_four_indent_spaces(line):
  result = re.match("^( *)",line)
  if (result != None and len(result.group(1)) % 2 != 0):
    return "indents should be two or four spaces, seeing {} spaces".format(len(result.group(1)))
  return None

def if_space(line):
  if(re.search("if\\(",line)):
    return "'if(' should be 'if ("
  return None
  
def function_call_space(line):
  result = re.search("(\\w+)\\s+(\\(.*)",line)
  if(result != None):
    return "'{}' should be '{}{}'".format(result.group(0),result.group(1),result.group(2))
  return None



#arithmeticInfixOp ::= ('+' | '-' | '*' | '/' | '%' | '\' | '.*' | './')
#logicalInfixOp :: ('||' | '&&' | '==' | '!=' | '<' | '<=' | '>' | '>=')
#assignment_op ::= '<-' | '=' | '+=' | '-=' | '*=' | '/=' | '.*=' | './='
#identifier ::= [a-zA-Z] [a-zA-Z0-9_]*
def space_around_operators(line):
  arg = "([a-zA-Z0-9_]+)"
  arithmetric_infix = "\\.\\*|\\./|[-+*/%]"
  logic_infix = r"\|\||&&|==|!=|<=|>=|>|<" 
  assignment_infix = "=" #"<-|=|+=|-=|*=|/=|.*=|./="
  infix = "(" + arithmetric_infix + "|" + logic_infix + "|" + assignment_infix + ")"
  #print(infix)
  result = re.match("^([^<>]*)<([^<>]*)>([^<>]*)",line) #"int real<lower=0,upper=42>" -> int real#lower=0,upper=42#
  if (result):
    line = result.group(1) + "#" + result.group(2) + "#" + result.group(3)
  result = re.search(arg + r"(\s*)" + infix + r"(\s*)" + arg, line)
  if (result != None and (result.group(2) == "" or result.group(4) == "")):
    return "spaces needed around operator {}".format(result.group(3))
  return None

#prefixOp ::= ('!' | '-' | '+' | '^')
def space_after_prefix_operator(line):
  arg = "([a-zA-Z0-9_]+)"
  result = re.search(arg + r"\s+([-+^])\s+" + arg, line) 
  if (result != None): #infix use of operator
    return None
  result = re.search(r"([!-+^])\s+" + arg, line)
  if (result != None):
    return "remove space after operator {}".format(result.group(1))
  return None

#postfixOp ::= '\''
def space_before_postfix_operator(line):
  arg = "([\\d\\w]+)" #overgenerates but should be ok after sucessful compile
  result = re.search(arg + "\\s+'", line)
  if (result != None):
    return "remove space before operator '"
  return None

def space_after_comma(line):
  num_dig = "([\\d\\w]+)"
  result = re.search(num_dig + "(\\([^)]+,)" + num_dig, line)
  if (result != None):
    return "add space after comma in function call {}{}".format(result.group(2),result.group(3))
  return None
  
def windows_cr_lf(line):
  if (re.search("\\r",line)):
    return True
  return False
  
def comment_block_start(line):
  if (re.match("^\\s*/[*]", line)):
    return True
  return False
  
def comment_block_end(line):
  if (re.match("^.*[*]/",line)):
    return True
  return False
  
def line_comment(line):
  if (re.match("^\\s*//",line)):
    return True
  return False
  
def line_comment_depreciated(line):
  if (re.match("^\\s*#",line)):
    return True
  return False

def lint_file(file_name):
  with io.open(file_name, 'r', newline='') as file_in:
    counter = 1
    in_comment_block = False
    #if (wrong_suffix(file_in.suffix()) != None):
    #  print(wrong_suffix(file_name))
    for line in file_in:
      num_plus_line = ":line number:{}='{}'".format(counter,line.rstrip())
    #need to skip comments
      if(comment_block_end(line)):
        in_comment_block = False
      if (in_comment_block):
        continue
      if(comment_block_start(line)):
        in_comment_block = True
        continue
      
      if(line_comment(line)):
        continue
      if(line_comment_depreciated(line)):
        print("# line comment depreciated {}".format(num_plus_line))
        continue
      
      if (white_space_comma(line) != None):
        print(white_space_comma(line) + num_plus_line)
      if (length_gt_80(line)!= None):
        print(length_gt_80(line) + num_plus_line)
      if(length_gt_65(line) != None):
        print(length_gt_65(line) + num_plus_line)
      if(lower_case_variables(line) != None):
        print(lower_case_variables(line) + num_plus_line)
      if(open_bracket_on_own_line(line) != None):
        print(open_bracket_on_own_line(line) + num_plus_line)
      if(multiple_statements_on_line(line) != None):
        print(multiple_statements_on_line(line) + num_plus_line)
      if(no_tabs(line) != None):
        print(no_tabs(line) + num_plus_line)
      if(two_or_four_indent_spaces(line) != None):
        print(two_or_four_indent_spaces(line) + num_plus_line)
      if(if_space(line) != None):
        print(if_space(line) + num_plus_line)
      if(function_call_space(line) != None):
        print(function_call_space(line) + num_plus_line)
      if(space_around_operators(line) != None):
        print(space_around_operators(line) + num_plus_line)
      if(space_after_prefix_operator(line) != None):
        print(space_after_prefix_operator(line) + num_plus_line)
      if(space_before_postfix_operator(line) != None):
        print(space_before_postfix_operator(line) + num_plus_line)
      #if (space_after_comma(line) != None):
      #  print(space_after_comma(line) + num_plus_line)
      if (windows_cr_lf(line)):
        print(r"Line contains Widows line termination'\r\n', please change to unix style '\n'" + num_plus_line)
      counter += 1

file_name = sys.argv[1]
print("linting " + file_name)
lint_file(file_name)
