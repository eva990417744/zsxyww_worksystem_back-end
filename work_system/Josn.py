from django.http import JsonResponse


class Json:
    ok = JsonResponse({'success': 'success'})
    error = JsonResponse({'error': 'error'})
    post_error = JsonResponse({'error': 'post pack error'})
    no_post = JsonResponse({'error': 'method no post'})

    def what_error(self, what):
        return JsonResponse({'error': what})

    def what_success(self, what):
        return JsonResponse({'success': what})

    def success(self, what):
        ok = {'success': 'success'}
        ok.update(what)
        return JsonResponse(ok)

    def failure(self, what):
        no = {'error': 'failure'}
        no.update(what)
        return JsonResponse(no)


json = Json()
