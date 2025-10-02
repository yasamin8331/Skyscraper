from collections import deque
from typing import Callable, List, Tuple


class CSP(object):
    """
    Represents a Constraint Satisfaction Problem (CSP).
    Attributes:
        variables (dict): A dictionary that maps variables to their domains.
        constraints (list): A list of constraints in the form of [constraint_func, variables].
        unassigned_var (list): A list of unassigned variables.
        var_constraints (dict): A dictionary that maps variables to their associated constraints.

    Methods:
        add_constraint(constraint_func, variables): Adds a constraint to the CSP.
        add_variable(variable, domain): Adds a variable to the CSP with its domain.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes a Constraint Satisfaction Problem (CSP) object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            variables (dict): A dictionary to store the variables of the CSP.
            constraints (list): A list to store the constraints of the CSP.
            unassigned_var (list): A list to store the unassigned variables of the CSP.
            var_constraints (dict): A dictionary to store the constraints associated with each variable.
            assignments (dict): A dictionary to store the assignments of the CSP.
        """
        self.variables = {}
        self.constraints = []
        self.unassigned_var = []
        self.var_constraints = {}
        self.assignments = {}
        self.assignments_number = 0

    def add_constraint(self, constraint_func: Callable, variables: List) -> None:
        """
        Adds a constraint to the CSP.

        Args:
            constraint_func (function): The constraint function to be added.
            variables (list): The variables involved in the constraint.

        Returns:
            None
        """
        """ You Should Code Here """
        self.constraints.append([constraint_func, variables])

        i = 0
        while i < len(variables):
            var = variables[i]
            if var not in self.var_constraints:
                self.var_constraints[var] = []
            self.var_constraints[var].append((constraint_func, variables))
            i += 1


    def add_variable(self, variable: any, domain: List) -> None:
        """
        Adds a variable to the CSP with its domain.

        Args:
            variable: The variable to be added.
            domain: The domain of the variable.

        Returns:
            None
        """
        """ You Should Code Here """
        self.variables[variable] = list(domain)
        self.unassigned_var.append(variable)
        self.assignments[variable] = None

    def assign(self, variable: any, value: any) -> None:
        """
        Assigns a value to a variable in the CSP.

        Args:
            variable (any): The variable to be assigned.
            value (any): The value to be assigned to the variable.

        Returns:
            nothing
        """
        
        """ You Should Code Here """
        self.assignments[variable] = value
        self.assignments_number += 1
        if variable in self.unassigned_var:
            self.unassigned_var.remove(variable)


    def is_consistent(self, variable: any, value: any) -> bool:
        """
        Checks if assigning a value to a variable violates any constraints.

        Args:
            variable (any): The variable to be assigned.
            value (any): The value to be assigned to the variable.

        Returns:
            bool: True if the assignment is consistent with the constraints, False otherwise.
        """

        """ You Should Code Here """
        constraints = self.var_constraints.get(variable, [])
        i = 0
        while i < len(constraints):
            constraint_func, vars_in_constraint = constraints[i]

            if constraint_func.__name__ == 'distinction_constraint':
                j = 0
                while j < len(vars_in_constraint):
                    var = vars_in_constraint[j]
                    if var != variable and self.assignments.get(var) == value:
                        print(f"distinction_constraint violated: {var} = {value}")
                        return False
                    j += 1
            else:
                all_assigned = True
                k = 0
                while k < len(vars_in_constraint):
                    if self.assignments.get(vars_in_constraint[k]) is None:
                        all_assigned = False
                        break
                    k += 1

                if all_assigned:
                    values = [self.assignments[var] for var in vars_in_constraint]
                    if not constraint_func(*values):
                        print(f"visibility constraint violated for variables {vars_in_constraint} with values {values}")
                        return False
            i += 1

        return True

        


    def is_complete(self) -> bool:
        """
        Checks if the CSP is complete, i.e., all variables have been assigned.

        Returns:
            bool: True if the CSP is complete, False otherwise.
        """
        return len(self.unassigned_var) == 0
    
    def is_assigned(self, variable: any) -> bool:
        """
        Checks if a variable has been assigned a value.

        Args:
            variable (str): The variable to check.

        Returns:
            bool: True if the variable has been assigned, False otherwise.
        """
        return self.assignments[variable] is not None

    def un_assign(self, removed_values_from_domain: List[Tuple[any, any]], variable: any) -> None:
        """
        Un assign a variable and restores its domain values.

        Args:
            removed_values_from_domain (list): A list of domain values to be restored.
            variable (any): The variable to be unassigned.

        Returns:
            None
        """
        """ You Should Code Here """

        self.assignments[variable] = None
        if variable not in self.unassigned_var:
            self.unassigned_var.append(variable)

    def remove_from_domain(self, removed: List[tuple]) -> None:
        i = 0
        while i < len(removed):
            var_name, removed_value = removed[i]
            if removed_value in self.variables[var_name]:
                self.variables[var_name].remove(removed_value)
            i += 1
