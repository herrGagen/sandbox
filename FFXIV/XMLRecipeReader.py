import xml.etree.ElementTree as ET


def get_recipe_from_xml(filename, recipename):
    root = ET.parse(filename)
    cp = int(root.find('cp').text)
    found_recipe = []
    for recipe in root.findall('recipe'):
        if (recipe.find('name').text).lower() == recipename.lower():
            found_recipe = recipe
            break
    if not found_recipe:
        raise KeyError("%s is not in the file %s" % (recipename, filename))
    durability = int(recipe.find('durability').text)
    careful_prog = int(recipe.find('careful_prog').text)
    total_prog = int(recipe.find('total_prog').text)
    num_mark = int(recipe.find('num_mark').text)
    stack_goal = int(recipe.find('stack_goal').text)
    return (cp,
            durability,
            careful_prog,
            total_prog,
            num_mark,
            stack_goal)


if __name__=="__main__":

    list = get_recipe_from_xml("gOlDsmithing.xml","Cloud Mica Whetstone")
    print(list)



