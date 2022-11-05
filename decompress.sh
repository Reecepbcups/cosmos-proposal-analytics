# mkdir -p compressed
# xz bank.json --keep &
# xz gov.json --keep &
# xz staking.json --keep &
# mv *.json.xz compressed

cd compressed
xz --decompress bank.json.xz --keep &
xz --decompress gov.json.xz --keep &
xz --decompress staking.json.xz --keep &
# then 
read -p "Press enter to continue after they all decompress"
cp *.json ../