#!/usr/bin/python

import sys
import gnomekeyring as gk


class Context(object):
    def clear(self):
        self.keychain = None
        self.name = None
        self.data = None
        self.attributes = {}
        self.kc_class = None
        

def find_entry( line, ctx ):
    ctx.clear()
    if line.startswith( "keychain:" ):
        ctx.keychain = line[11:-1]
        return parse_class
    return find_entry

def parse_class( line, ctx ):
    if line.startswith( "class:" ):
        ctx.kc_class = line[7:-1]
        return parse_attributes
    return parse_class

def parse_attributes( line, ctx ):
    if line.startswith( "    " ) or line.startswith( "attributes:" ):
        line = line.strip()
        if line.startswith( '"' ):
            (key,val) = line.split( "=", 1 )
            # TODO: Make this actually parse the attributes, pull out the entry name and store the rest in ctx.attributes
            if key.startswith('"svce"<blob>'):
                # Name
                ctx.name = val.replace('"','')
        return parse_attributes
    return parse_data

def parse_data( line, ctx ):
    if ctx.name is not None:
        publish( ctx, line.replace('"','') )
    return find_entry

def publish( ctx, secret ):
    gk.item_create_sync( gk.get_default_keyring_sync(), gk.ITEM_GENERIC_SECRET, ctx.name, ctx.attributes, secret, False )


def import_keychain( path ):
    state = find_entry
    ctx = Context()

    with open( path ) as f:
        for line in f:
            state = state(line, ctx)

if __name__ == "__main__":
    if len(sys.argv) is not 2:
        print "kc-import <OS X KeyChain export>"
        sys.exit(0)

    import_keychain( sys.argv[1] )


