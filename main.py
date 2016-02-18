import sys
import os.path


def main():
    # Read command line arguments
    args = sys.argv[1:]
    # More than 1 argument supplied
    if len(args) > 0:
        # Get data filename
        filename = args[0]
        # Bags
        bags = {}
        # Generic bag info
        bag_info = {}
        # Items
        items = {}
        # Section tracker
        current_section = 0
        # Read each line and add to the examples and output lists
        if os.path.isfile(filename):
            with open(filename, "r") as infile:
                for line in infile:
                    # Remove new line character and carriage return
                    line = line[:-1]
                    # If the line is a comment, increment the section counter
                    if line[:5].strip() == "#####":
                        current_section += 1
                    else:
                        s = line.split(" ")
                        if current_section == 1: # Items
                            name = s[0]
                            weight = s[1]
                            items[name] = {"weight": weight}
                        elif current_section == 2: # Bags
                            name = s[0]
                            capacity = s[1]
                            bags[name] = {"capacity": capacity}
                        elif current_section == 3: # Fitting limits
                            lower_bound = s[0]
                            upper_bound = s[1]
                            bag_info["lower_bound"] = lower_bound
                            bag_info["upper_bound"] = upper_bound
                        elif current_section == 4: # Unary inclusive
                            name = s[0]
                            bags = s[1:]
                            if not items.has_key("require_bags"):
                                items[name]["require_bags"] = []
                            for b in bags:
                                if b:
                                    items[name]["require_bags"].append(b)
                        elif current_section == 5: # Unary exclusive
                            name = s[0]
                            bags = s[1:]
                            if not items.has_key("reject_bags"):
                                items[name]["reject_bags"] = []
                            for b in bags:
                                if b:
                                    items[name]["reject_bags"].append(b)
                        elif current_section == 6: # Binary equals
                            item1 = s[0]
                            item2 = s[1]
                            items[item1]["equals"] = item2
                            items[item2]["equals"] = item1
                        elif current_section == 7: # Binary not equals
                            item1 = s[0]
                            item2 = s[1]
                            items[item1]["not_equals"] = item2
                            items[item2]["not_equals"] = item1
                        elif current_section == 8: # Binary
                            item1 = s[0]
                            item2 = s[1]
                            value1 = s[2]
                            value2 = s[3]
                            # Should be read as:
                            # item1 = value1 if item2 = value2
                            items[item1]["mutex"] = [value1, item2, value2]
                            items[item2]["mutex"] = [value2, item1, value1]
                # print bag_info
                # print bags
                print items

        else:
            # Throw error when cannot open file
            print("Input file does not exist.")
    else:
        # Show usage when not providing enough argument
        print("Usage: python main.py <filename>")

if __name__ == "__main__":
    main()
