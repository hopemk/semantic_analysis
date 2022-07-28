from django.shortcuts import render

# Create your views here.
def classify(request):
    if request.method == 'POST':
        emri = request.POST.get('name')
        email = request.POST.get('e-mail')
        numri_tel = request.POST.get('phone')
        prof = request.user.profile
        kerkesa = Kerkesat(profili=prof, emri=emri, email=email, numri_tel=numri_tel)
        kerkesa.save()
        prof_id = prof.id
        Pro.objects.filter(id=prof_id).update(is_teacher=True)
        
        message = 'Kerkesa juaj per nje llogari mesuesi u pranua! Tani ju mund te ktheheni tek MesoOn dhe te ngarkoni kurse dhe leksione, pune te mbare!'
        send_mail(
            'MesoOn, kerkesa u pranua.',
            message,
            'mesoon@no-reply.com',
            [email],
            fail_silently=False,
        )
        send_mail(
            'MesoOn',
            'Dikush beri kerkese per llogari mesuesi. Me info: ' + emri + ' , ' + email + ' , ' + numri_tel + ' , ' + str(prof) + '.',
            'mesoon@no-reply.com',
            ['redian1marku@gmail.com'],
            fail_silently=False,
        )
        messages.info(request, f'Kerkesa u dergua me sukses, ju do te njoftoheni me email.')
        return redirect('courses:home')

