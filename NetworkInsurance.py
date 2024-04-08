import os


# This function will loop through line by line to get the Product name and relevant companies
def scrape():
    # Open the pdf
    with open("C:\\Users\\Noricum\\Downloads\\NetworkInsuranceCarriers.txt") as file:
        product_list = {}
        current_product = ""
        # loop through the lines
        for line in file:
            line = line.strip()
            # if the line is all caps it is a product name
            if line.isupper():
                current_product = line
                product_list[current_product] = []  # Add the product to the product list
                # print("Product: " + line)
            # if the line is not all caps, it is a company name
            elif current_product is not None:
                product_list[current_product].append(line)  # Append the company to the product list
                # print("Company" + line)
        print(product_list)
        # fix product_list to be a json object
        product_list = str(product_list).replace("'", "\"")  # Replace single quatations with double quotations
        # Save the product list to a file
        with open("C:\\Users\\Noricum\\Downloads\\NetworkInsuranceCarriers.json", "w") as output:
            output.write(str(product_list))
            print("File Saved")


scrape()
