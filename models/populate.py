# -*- coding: utf-8 -*-
    
if db(db.markup).isempty():
    db.markup.bulk_insert([{'name':'markmin'},
                           {'name':'html'}
                           ])

if db(db.place).isempty():
    db.place.bulk_insert([{'name':'blogpost'},
                          {'name':'sidebar'},
                          {'name':'página'},
                          {'name':'documento'}
                          ])
