# -*- coding: utf-8 -*-
    
if db(db.markup).isempty():
    db.markup.bulk_insert([{'name':'markmin'},
                           {'name':'html'},
                           {'name':'template'},
                           ])

if db(db.place).isempty():
    db.place.bulk_insert([{'name':'blog'},
                          {'name':'sidebar'},
                          {'name':'page'},
                          {'name':'doc'}
                          ])
