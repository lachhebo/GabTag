RELEASE_DATE=$(date +%Y-%m-%d)
LATEST_VERSION=$(git describe --tags --abbrev=0 2>/dev/null | sed -En 's/v//p') 
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null) 
RELEASE_NUMBER="${1}"

## update version information

sed -i 's/version="'${LATEST_VERSION}'"/version="'${RELEASE_NUMBER}'"/g' data/com.github.lachhebo.Gabtag.appdata.xml.in
sed -i 's/release date="'[1234567890-]*'"/release date="'${RELEASE_DATE}'"/g' data/com.github.lachhebo.Gabtag.appdata.xml.in
sed -i 's/'${LATEST_VERSION}'/'${RELEASE_NUMBER}'/g'  src/version.py


## commit those modification and create a new release tag
git commit -am 'upgrade version to '${RELEASE_NUMBER}
git tag -a ${RELEASE_NUMBER} -m "version"${RELEASE_NUMBER}
git push
git push --tags


## clone flathub repo and update manifest to match latest tags

git clone https://github.com/flathub/com.github.lachhebo.Gabtag.git
cd com.github.lachhebo.Gabtag
sed -i 's/"tag": "'${LATEST_TAG}'"/"tag": "'${RELEASE_NUMBER}'"/g' com.github.lachhebo.Gabtag.json
git commit -am "upgrade to new verson "${RELEASE_NUMBER}
git push https://lachhebo:${PASSWORD_DEPLOYEMENT}@github.com/flathub/com.github.lachhebo.Gabtag.git
