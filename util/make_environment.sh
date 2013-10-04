
echo "Cloning git repositories used in project ..."
echo

mkdir git

cd git 
git clone git@github.com:bireme/iahx-controller.git iahx-controller
git clone git@github.com:bireme/iahx-opac.git iahx-opac

git clone git@github.com:scieloorg/search-books.git search-books
git clone git@github.com:scieloorg/search-journals.git search-journals

cd ..

echo "Creating web environment..."
echo

# web environment
mkdir web
cd web

echo "Creating search BOOKS environment..."
echo

# BOOKS environment
cp -r ../git/iahx-opac/ books
cd books
rm -rf .git
# make directory for search logs
mkdir logs
chmod o+w logs

# copy configuration file
cd config
cp ../../../git/search-books/iahx/config/config-DEV.xml config.xml
cd ..
# make symbolic links for core files
rm -rf lib
ln -s ../../git/iahx-opac/lib lib
rm -rf locale
ln -s ../../git/search-books/iahx/locale locale
rm -rf views
ln -s ../../git/iahx-opac/views views
rm -rf templates
mkdir templates
cd templates
ln -s ../../../git/iahx-opac/templates/* .
rm custom
ln -s ../../../git/search-books/iahx/templates/custom custom
cd ..
cd static
rm -rf *
ln -s ../../../git/search-books/iahx/static/css css
ln -s ../../../git/search-books/iahx/static/image image
ln -s ../../../git/iahx-opac/static/js js
ln -s ../../../git/iahx-opac/static/swf swf
cd ..
cd ..

echo "Creating search JOURNALS environment..."
echo

# JOURNALS environment
cp -r ../git/iahx-opac/ journals
cd journals
rm -rf .git
# make directory for search logs
mkdir logs
chmod o+w logs

# copy configuration file
cd config
cp ../../../git/search-journals/iahx/config/config-DEV.xml config.xml
cd ..
# make symbolic links for core files
rm -rf lib
ln -s ../../git/iahx-opac/lib lib
rm -rf locale
ln -s ../../git/search-journals/iahx/locale locale
rm -rf views
ln -s ../../git/iahx-opac/views views
rm -rf templates
mkdir templates
cd templates
ln -s ../../../git/iahx-opac/templates/* .
rm custom
ln -s ../../../git/search-journals/iahx/templates/custom custom
cd ..
cd static
rm -rf *
ln -s ../../../git/search-journals/iahx/static/css css
ln -s ../../../git/search-journals/iahx/static/image image
ln -s ../../../git/iahx-opac/static/js js
ln -s ../../../git/iahx-opac/static/swf swf


echo "Done"
echo

