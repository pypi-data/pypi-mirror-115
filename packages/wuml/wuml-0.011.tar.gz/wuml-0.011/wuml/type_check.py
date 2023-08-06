

def correct_variable_type(variable, intended_type):
	if type(variable).__name__ == intended_type: return True
	return False
