# convert Jupyter Notebooks to Python scripts
jupyter nbconvert --to script docs/bokeh*.ipynb
jupyter nbconvert --to script docs/geopandas.ipynb
jupyter nbconvert --to script docs/rioxarray*.ipynb

# remove "# In []" and multiple blank lines
for f in docs/*.py;
do sed -i -e '/^# In\[/d' $f
cat -s $f > $f.txt
mv $f.txt $f
done

# format scripts
black -l 79 docs/*.py

mv docs/*.py charts/python/
