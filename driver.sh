# if ! [[ "18.04 20.04 22.04 23.04" == *"$(lsb_release -rs)"* ]];
# then
#     echo "Ubuntu $(lsb_release -rs) is not currently supported.";
#     exit;
# fi

# curl https://packages.microsoft.com/keys/microsoft.asc |  tee /etc/apt/trusted.gpg.d/microsoft.asc

# curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list |  tee /etc/apt/sources.list.d/mssql-release.list

#  apt-get update
#  ACCEPT_EULA=Y apt-get install -y msodbcsql18
# # optional: for bcp and sqlcmd
#  ACCEPT_EULA=Y apt-get install -y mssql-tools18
# echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
# source ~/.bashrc
# # optional: for unixODBC development headers
#  apt-get install -y unixodbc-dev
# Replace '20.04' with the version of Ubuntu you're using that is supported
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
apt-get update
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list |  tee /etc/apt/sources.list.d/mssql-release.list

 apt-get update
 ACCEPT_EULA=Y apt-get install -y msodbcsql18
# optional: for bcp and sqlcmd
 ACCEPT_EULA=Y apt-get install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
 apt-get install -y unixodbc-dev