"Example showing how to add a column on a existing column"

from tables import *

class Particle(IsDescription):
    name        = StringCol(16, pos=1)   # 16-character String
    lati        = Int32Col(pos=2)        # integer
    longi       = Int32Col(pos=3)        # integer
    pressure    = Float32Col(pos=4)    # float  (single-precision)
    temperature = Float64Col(pos=5)      # double (double-precision)

# Open a file in "w"rite mode
fileh = openFile("add-column.h5", mode = "w")
# Create a new group
group = fileh.createGroup(fileh.root, "newgroup")

# Create a new table in newgroup group
table = fileh.createTable(group, 'table', Particle, "A table", Filters(1))

# Append several rows
table.append([("Particle:     10", 10, 0, 10*10, 10**2),
              ("Particle:     11", 11, -1, 11*11, 11**2),
              ("Particle:     12", 12, -2, 12*12, 12**2)])

print "Contents of the original table:", fileh.root.newgroup.table[:]

# close the file
fileh.close()

# Open it again in append mode
fileh = openFile("add-column.h5", "a")
group = fileh.root.newgroup
table = group.table

# Get a description of table in dictionary format
descr = table.description._v_colObjects
descr2 = descr.copy()

# Add a column to description
descr2["hot"] = BoolCol(dflt=False)

# Create a new table with the new description
table2 = fileh.createTable(group, 'table2', descr2, "A table", Filters(1))

# Copy the user attributes
table.attrs._f_copy(table2)

# Fill the rows of new table with default values
for i in xrange(table.nrows):
    table2.row.append()
# Flush the rows to disk
table2.flush()

# Copy the columns of source table to destination
for col in descr:
    getattr(table2.cols, col)[:] = getattr(table.cols, col)[:]

# Fill the new column
table2.cols.hot[:] = [ row["temperature"] > 11**2 for row in table ]

# Remove the original table
table.remove()

# Move table2 to table
table2.move('/newgroup','table')

# Print the new table
print "Contents of the table with column added:", fileh.root.newgroup.table[:]

# Finally, close the file
fileh.close()
