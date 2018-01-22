from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
@login_required
def index(request):

    #retrieve MOCA session
    moca = request.session['moca']

    #get current shipment data and parse it into JSON format
    _ , res = moca.execute("""[select dscmst.lngdsc shpsts,
                                count(1) count
                               from shipment,
                                    dscmst
                                where shipment.shpsts = dscmst.colval
                                  and dscmst.colnam = 'shpsts'
                                  and shipment.shpsts not in ('C', 'B')
                                group by dscmst.lngdsc]""")


    ship_list = []

    for _ , row in res.iterrows():

        entry = {"label" : row['shpsts'], "value": row['count']}
        ship_list.append(entry.copy())

    data = json.dumps(ship_list)

    #get user productivity data and parse into JSON format
    _ , res = moca.execute("""[select usr_id,
                                 count(1) transactions
                                from dlytrn
                                where rownum < 20000
                                group by usr_id
                                order by 1]""")

    trn_list = [{"key": "Transactions", "color": "#0000ff"}]
    values = []

    for _ , row in res.iterrows():

        entry = {"label" : row['usr_id'], "value": row['transactions']}
        values.append(entry.copy())

    trn_list[0].update({'values': values})

    user_data = json.dumps(trn_list)

    #get outstanding shipment data and parse into JSON format
    _ , res = moca.execute("""list shipments
                                where wh_id = @@wh_id
                               and shpsts = 'R'
                               and [rownum < 8]
                              |
                              publish data
                                where ship_id = @ship_id
                               and client_id = @client_id
                               and carcod = @carcod
                               and srvlvl = @srvlvl""")

    table_list = res.to_dict('records')

    #get current counts from various tables
    _ , res = moca.execute("""[select count(1) shorts
                                from rplwrk]""")

    shorts = res['shorts'][0]
    shorts = int(float(shorts))

    _ , res = moca.execute("""[select count(1) picks
                                from pckwrk_view
                               where wrktyp = 'P'
                                and appqty != pckqty]""")

    picks = res['picks'][0]
    picks = int(float(picks))

    _ , res = moca.execute("""[select count(1) orders
                                from ord
                               where trunc(adddte) = trunc(sysdate)]""")

    orders = res['orders'][0]
    orders = int(float(orders))

    #save moca session again in case session key has been updated
    request.session['moca'] = moca

    return render(request, 'index.html', {"data": data, "table_list" : table_list, "user_data": user_data, "shorts": shorts, "picks": picks, "orders": orders })
