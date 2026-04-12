def has_role(payload, role):
    '''Return True if the authenticated user has the specified role.'''
    if payload is None:
        return False
    
    return payload.get('role') == role
