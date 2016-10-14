while :
    do
        python run.py 2>&1 | tee -a output/bot.txt
        sleep 5
        echo ""
        echo "============================================================"
        echo "                         RESTARTING"
        echo "============================================================"
        echo ""
done
