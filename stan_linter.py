import io
import re
import sys


file_name = sys.argv[1]

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

#see Variable Naming in Stan User's Guide, lowercase_w_underscore, 
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
  result = re.match("^(\\s*)",line)
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

def space_around_operators(line):
  arg = "([\\d\\w]+)" #overgenerates but should be ok after sucessful compile
  arithmetric_infix = "\\.\\*|\\./|[-+*/%]"
  logic_infix = "\\|\\||&&|==|!=|<=|>=|>|<"
  infix = "(" + arithmetric_infix + "|" + logic_infix + ")"
  result = re.search(arg + infix + arg, line)
  if (result != None):
    return "spaces needed around operator {}".format(result.group(2))
  result = re.search(arg + "\\s" + infix + arg, line)
  if (result != None):
    return "spaces needed around operator {}".format(result.group(2))
  result = re.search(arg + infix + "\\s" + arg, line)
  if (result != None):
    return "spaces needed around operator {}".format(result.group(2))
  return None

#prefixOp ::= ('!' | '-' | '+' | '^')
def space_after_prefix_operator(line):
  arg = "([\\d\\w]+)" #overgenerates but should be ok after sucessful compile
  result = re.search("([!-+^])\\s+" + arg, line)
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
    return "windows lf"
  return None
  

io.open(file_name, 'r', newline='').readlines()


#with open(file_name) as file_in:
with io.open(file_name, 'r', newline='') as file_in:
  counter = 1
  for line in file_in:
    #need to skip comments
    if (len(line) > 80):
      print("line {} longer than 80 chars ,".format(counter))
    if (white_space_comma(line) != None):
        print(white_space_comma(line))
    if (lower_case_variables(line) != None):
        print(lower_case_variables(line))
    counter += 1
