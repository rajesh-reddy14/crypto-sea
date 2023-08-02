rname='jom_ariya', password='123456789', name='Ariya')
    db.session.add(new_user)

    new_user_2 = Users(username='earth_ekaphat', password='123456789', name='Ekaphat')
    new_user_3 = Users(username='bonus_ekkawit', password='123456789', name='Ekkawit')
    db.session.add(new_user_2)
    db.session.add(new_user_3)