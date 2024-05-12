# convert Jupyter Notebooks to Python scripts
jupyter nbconvert --to script docs/python/*.ipynb

# remove "# In []" and multiple blank lines
for f in docs/python/*.py;
do sed -i -e '/^# In\[/d' $f
cat -s $f > $f.txt
mv $f.txt $f
done

# move to a different directory
mv docs/python/*.py charts/python/
