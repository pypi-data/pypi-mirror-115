def is_string(arg: any) -> bool:
    """Checks if an argument is a string

        Parameters
        ----------
        arg
            A variable of any type to be checked

        Returns
        -------
        bool
            True if the provided argument is a string, otherwise False
        """
    return isinstance(arg, str)
