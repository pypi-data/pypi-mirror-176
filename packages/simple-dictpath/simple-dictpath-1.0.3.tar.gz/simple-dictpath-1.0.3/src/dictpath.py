from typing import Optional, Any


class dictp(dict):
    """
    Provides a simple path-like access to nested dictionary elements
    See README: https://github.com/pathtofile/dictpath

    """

    def __getitem__(self, key):
        """
        Overload getter to also treat any sub-dicts as dictp
        """
        item = super().__getitem__(key)
        if type(item) == dict:
            return dictp(item)
        else:
            return item

    def __call__(
        self,
        path: str,
        value_if_missing: Optional[Any] = None,
        raise_if_missing: bool = False,
        drop_missing: bool = False,
        raw_index: bool = False,
    ) -> Optional[Any]:
        """
        Lookup subkeys by path

        Parameters:
            path (str): Path string to lookup, e.f. "first/second/0/val"
            value_if_missing (Optional[Any]): Default value to return if subkey doesn't exist. Default returns None
            drop_missing (bool): When returning elements in a list, don't return any that don't have the requested subkey
            raw_index (bool): Overide list slicing to access a key that contains a ':' character

        Returns:
            Any subkey/s matching path, otherwise value_if_missing
        """
        # Handle basic cases
        if path == "":
            return self
        parts = path.split("/")
        try:
            # Enumerate through pointer path
            node = self
            for i, part in enumerate(parts):
                if type(node) == list:
                    if raw_index:
                        # raw_index doesn't try to coalece list indexes
                        node = node[part]
                    elif ":" in part:
                        # If using a list wildcard, we need to re-create the list
                        new_path = "/".join(parts[i + 1 :])
                        new_nodes = []

                        start, end = part.split(":")
                        if start == "":
                            start = "0"
                        if end == "":
                            end = f"{len(node)}"
                        start = int(start)
                        end = int(end)

                        for child in node[start:end]:
                            if type(child) == dict:
                                # Need to recurse into dictionary
                                new_val = dictp(child)(
                                    new_path, value_if_missing, drop_missing
                                )
                                if (new_val != value_if_missing) or (not drop_missing):
                                    new_nodes.append(new_val)
                            else:
                                new_nodes.append(child)
                        return new_nodes
                    else:
                        # Assume part is a number for the index
                        node = node[int(part)]
                elif type(node[part]) == dict:
                    node = dictp(node[part])
                else:
                    node = node[part]
            return node
        except (KeyError, ValueError):
            if raise_if_missing:
                raise
            else:
                return value_if_missing
