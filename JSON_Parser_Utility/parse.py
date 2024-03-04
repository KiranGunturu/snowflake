import json
json_data={
"id":2,
"first_name":"Dag",
"last_name":"Croney",
"gender":"Male",
"city":"Louny",
"job":{"title":"Clinical Specialist","salary":43000},
"spoken_languages":[{"language":"Assamese","level":"Basic"},{"language":"Papiamento","level":"Expert"},{"language":"Telugu","level":"Basic"}],
"prev_company":["MacGyver, Kessler and Corwin","Gerlach, Russel and Moen"]
}

json_data_list = [json_data]
print(json_data_list)
#res = json.dumps(json_data)
#print(res)
