
public_paths = {"/login/google", "/logout", "/", "/login/google/authorized", "/index"}

def check_security(request):
    print(request.path, "security")
    path = request.path
    good_to_go = False
    if path in public_paths:
        good_to_go = True
    return good_to_go
