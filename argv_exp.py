import sys

# Set default values if no alpha is provided
in_alpha = 0.5
alpha = 0.5 if float(in_alpha) is None else float(in_alpha)

# Set default values if no l1_ratio is provided
in_l1_ratio = 0.7
l1_ratio = 0.5 if float(in_l1_ratio) is None else float(in_l1_ratio)


print(alpha, l1_ratio)
