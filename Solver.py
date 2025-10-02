from collections import deque
from typing import Callable, List, Tuple, Any
from CSP import CSP



class Solver(object):

    def __init__(self, csp: CSP, domain_heuristics: bool = False, variable_heuristics: bool = False, MAC: bool = False) -> None:
        """
        Initializes a Solver object.

        Args:
            csp (CSP): The Constraint Satisfaction Problem to be solved.
            domain_heuristics (bool, optional): Flag indicating whether to use domain heuristics. Defaults to False.
            variable_heuristics (bool, optional): Flag indicating whether to use variable heuristics. Defaults to False.
            AC_3 (bool, optional): Flag indicating whether to use the AC-3 algorithm. Defaults to False.
            MAC (bool, optional): Flag indicating whether to use the MAC algorithm. Defaults to False.
        """
        self.domain_heuristic = domain_heuristics
        self.variable_heuristic = variable_heuristics
        self.MAC = MAC
        self.csp = csp

        self.board_size = int(len(self.csp.variables) ** 0.5)


    def backtrack_solver(self) -> None | dict:
        """
        Backtracking algorithm to solve the constraint satisfaction problem (CSP).

        Returns:
            dict{any : any}: A list of variable-value assignments that satisfy all constraints.
        """

        """ You Should Code Here """

        if self.csp.is_complete():
            print("Solution Assignments:")
            for key, value in self.csp.assignments.items():
                print(f"{key} = {value}")
            solution = self.csp.assignments.copy()
            return solution

        
            
        
        var = self.select_unassigned_variable()
        domain = self.ordered_domain_value(var)

        for value in domain:
            print(f"Assuming {var} = {value}")
            removes_to_reverse_in_unassign = list()
            self.csp.assign(var, value)
            print(f"    {var} = {value} assigned")
            if self.csp.is_consistent(var, value):
                solution = self.backtrack_solver()
                if solution != None:
                    return solution
                removes_to_reverse_in_unassign.append((var, value))
                self.csp.un_assign(removes_to_reverse_in_unassign, var)
                print(f"    {var} = {value} unassigned")
                print(f"We conclude {var} != {value}")
            else:
                removes_to_reverse_in_unassign.append((var, value))
                self.csp.un_assign(removes_to_reverse_in_unassign, var)
                print(f"    {var} = {value} unassigned")
                print(f"{var} != {value} because of inconsistency")

        return None

    def select_unassigned_variable(self) -> any:
        """
        Selects an unassigned variable using the MRV heuristic or Random.

        Returns:
            any: The selected unassigned variable.
        """

        """ You Should Code Here """
        if self.variable_heuristic:
            return self.MRV(self.csp.unassigned_var)

        return self.csp.unassigned_var[0]

    def ordered_domain_value(self, variable: str) -> Any:
        """
        Returns a list of domain values for the given variable in a specific order.

        Args:
            variable (any): The name of the variable.

        Returns:
            List[any]: A list of domain values for the variable in a specific order.
        """
        """ You Should Code Here """
        if self.domain_heuristic:
            return self.LCV(variable)
        
        return self.csp.variables[variable]




    def apply_MAC(self) -> List[Any]:
        """
        Applies the Maintaining Arc Consistency (MAC) algorithm to the CSP.

        This function processes all constraints in the CSP to remove values
        from the domains of variables that are inconsistent with the constraints.

        Returns:
            List[Any]: A list of values that were removed from the domains of variables.
        """

        """ You Should Code Here """
        constraint_arcs = deque(self.csp.constraints)
        
        values_to_remove = []
        while constraint_arcs:
            constraint, variables = constraint_arcs.popleft()
            removed_values = self.multi_arc_reduce(variables, constraint)
            if removed_values:
                values_to_remove.extend(removed_values)

                for var in variables:
                    for con, vars_in_con in self.csp.var_constraints[var]:
                        if con != constraint:
                            constraint_arcs.append([con, vars_in_con])
        return values_to_remove
    
    def combinations(self, variables: List[str], value_x: Any) -> List[tuple]:
        combinations = []
        domains = [self.csp.variables[var] for var in variables]

        stack = [(0, [])]  

        while stack:
            index, current_combination = stack.pop()

            if index == len(domains):
                combinations.append((value_x, *current_combination))
                continue

            i = len(domains[index]) - 1
            while i >= 0:  
                value = domains[index][i]
                stack.append((index + 1, current_combination + [value]))
                i -= 1

        return combinations



    def multi_arc_reduce(self, constraint_func: callable, variables: List[Any]) -> List[Tuple[Any, Any]]:
        """
        Reduces the domains of variables based on the specified constraint.

        This function examines the current assignments of the given variables
        and removes values from their domains that are inconsistent with the
        provided constraints, specifically in relation to clues and prefixes.

        Args:
            constraint_func (Callable): The constraint function that defines the
                                         relationship between the variables.
            variables (List[Any]): A list of variable names whose domains are
                                   to be reduced.

        Returns:
            List[Tuple[Any, Any]]: A list of tuples where each tuple contains
                                    a variable name and a value that was removed
                                    from the variable's domain.
        """
        """ You Should Code Here """

        removed_values = list()

        i = 0
        while i < len(variables):
            x = variables[i]
            ys = [v for v in variables if v != x]

            j = 0
            while j < len(self.csp.variables[x]):
                value = self.csp.variables[x][j]
                satisfied = False

                combinations = self.combinations(ys, value)
                k = 0
                while k < len(combinations):
                    if constraint_func(*combinations[k]) == True:
                        satisfied = True
                        break
                    k += 1

            if not satisfied:
                self.csp.variables[x].remove(value)
                removed_values.append((x, value))
            else:
                j += 1

        if removed_values:
            return removed_values

        i += 1

        return None


    def binary_arc_reduce(self, x: Any, y: Any, constraint_func: callable) -> list[Any] | None:
        """
        Reduce the domain of variable x based on the constraints between x and y.

        This function checks the values in the domain of variable x and removes
        any values that are inconsistent with the values in the domain of variable y
        according to the specified constraint function.

        Args:
            x (Any): The first variable whose domain is being reduced.
            y (Any): The second variable used to check constraints against x.
            constraint_func (callable): A function that checks the consistency
                                         between two values.

        Returns:
            list[Any] | None: A list of deleted values from the domain of variable x
                              if any values were removed, None otherwise.
        """

        """ You Should Code Here """

        return None
    
    def MRV(self, variables) -> Any:
        """
        Selects the variable with the Minimum Remaining Values (MRV) heuristic.

        Returns:
            Any: The variable with the fewest remaining values.
        """
        """ You Should Code Here """

        mrv_variable = variables[0]
        mrv_variable_domain_length = len(self.csp.variables[mrv_variable])

        i = 0
        while i < len(variables):
            variable = variables[i]
            if len(self.csp.variables[variable]) < mrv_variable_domain_length:
                mrv_variable = variable
                mrv_variable_domain_length = len(self.csp.variables[variable])
            i += 1

        return mrv_variable


    def LCV(self, variable: Any) -> List[any]:
        """
        Orders the values of a variable based on the Least Constraining Value (LCV) heuristic.

        Args:
            variable (Any): The variable for which to order the values.

        Returns:
            List[Any]: A list of values sorted based on the number of constraints they impose.
        """
        """ You Should Code Here """
        def count_constraints(value):
            constraining_effect = 0

            for _, vars_in_constraint in self.csp.var_constraints.get(variable, []):
                for var in vars_in_constraint:
                        if var != variable:
                            
                            if value in self.csp.variables[var]:
                                constraining_effect += 1
            
            return constraining_effect

        
        return sorted(self.csp.variables[variable], key=lambda val: count_constraints(val))

