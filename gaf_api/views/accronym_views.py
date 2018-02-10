
# @view_config(route_name="v1:acronyms", request_method="GET", context=Root)
# def get_acronyms(request: Request):
#     db.cursor.execute("SELECT acronym FROM public.acronyms")
#     acronyms = db.cursor.fetchall()
#     return acronyms
#
#
# @view_config(route_name="v1:acronyms/new", request_method="POST", context=Root)
# def add_acronym(request: Request):
#     acronym = request.json_body["acronym"]
#     acronym_test = acronym.split()
#     if not len(acronym_test) > 3:
#         if acronym_test[0][0].lower() == "g":
#             if acronym_test[1][0].lower() == "a":
#                 if acronym_test[2][0].lower() == "f":
#                     db.cursor.execute("SELECT acronym FROM public.acronyms")
#                     acc = db.cursor.fetchall()
#                     for i in acc:
#                         if i[0].lower() == acronym.lower():
#                             return {"status": "Acronym already exists"}
#                     db.cursor.execute("INSERT INTO public.acronyms (acronym) VALUES (%s)", (acronym, ))
#                     db.conn.commit()
#                     return {"status": "Added acronym"}
#     return {"status": "Invalid acronym"}

