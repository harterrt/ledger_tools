set -e

# Download new transactions
rm -f ~/Downloads/transactions.csv
firefox-trunk \
    'https://wwws.mint.com/transactionDownload.event?queryNew=&offset=0&filterType=cash&comparableType=4'
sleep 3

# Refresh the canonical ledger file
cd /home/harterrt/Private/account_data
./combine

cd /home/harterrt/Documents/ledger_tools

# Identify new transactions
python3 -m ledgertools.cli dump-new-trans \
	--mint ~/Downloads/transactions.csv \
	--ledger ~/Private/account_data/.combined \
	--out ~/Private/account_data/new.pickle

# Enter categorization
python3 -m ledgertools.cli categorize \
	--new ~/Private/account_data/new.pickle \
	--ledger ~/Private/account_data/.combined \
	--out ~/Private/account_data/ledger/new.ledger
