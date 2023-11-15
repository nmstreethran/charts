jupyter nbconvert --sanitize-html --to notebook --inplace docs/python/*.ipynb

# convert Jupyter Notebooks to Python scripts
jupyter nbconvert --to script docs/python/*.ipynb

# remove "# In []" and multiple blank lines
for f in docs/python/*.py;
do sed -i -e '/^# In\[/d' $f
cat -s $f > $f.txt
mv $f.txt $f
done

# format scripts
black -l 79 docs/python/*.py

# sort imports
isort docs/python/*.py

# move to a different directory
mv docs/python/*.py charts/python/
