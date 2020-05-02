from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date

# Create your views here.


def index(request):
    return render(request, 'store/index.html')


def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None,  # set this to an instance of the required book
        # set this to the number of copies of the book available, or 0 if the book isn't available
        'num_available': None,
    }
    # START YOUR CODE HERE
    context['book'] = Book.objects.get(pk=bid)
    specificBook = BookCopy.objects.filter(book=bid, status=False)
    context['num_available'] = specificBook.count()

    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None,  # set this to the list of required books upon filtering using the GET parameters
        # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    # START YOUR CODE HERE
    context['books'] = Book.objects.all()

    return render(request, template_name, context=context)


@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    context['books'] = BookCopy.objects.filter(borrower=request.user)

    return render(request, template_name, context=context)


@csrf_exempt
@login_required
def loanBookView(request):
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    # START YOUR CODE HERE
    book_id = request.POST['bid']  # get the book id from post data
    booksOfThatId = BookCopy.objects.filter(book=book_id, status=False)
    if booksOfThatId.count() != 0:
        singleBook = booksOfThatId[0]
        singleBook.borrower = request.user
        singleBook.borrow_date = date.today()
        singleBook.status = True
        singleBook.save()
        response_data['message'] = "success"

    else:
        response_data['message'] = "faliure"

    return JsonResponse(response_data)


'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
'''
@csrf_exempt
@login_required
def returnBookView(request):
    response_data = {
        'message': None,
    }
    key = request.POST['bId']
    try:
        singleBook = BookCopy.objects.get(pk=key)
        singleBook.borrower = None
        singleBook.borrow_date = None
        singleBook.status = False
        singleBook.save()
        response_data['message'] = "success"
    except:
        response_data['message'] = "faliure"

    return JsonResponse(response_data)


@csrf_exempt
@login_required
def userRatingView(request, id):
    if request.method == "POST":
        urating = request.POST['urating']
        book = Book.objects.get(pk=id)
        rating = UserRatings()
        rating.book = book
        rating.user = request.user
        rating.rating = urating
        prevRating = UserRatings.objects.filter(user=request.user, book=book)
        prevRating.delete()
        rating.save()
        allBooksOfThatName = UserRatings.objects.filter(book=book)
        sum = 0
        for particularBook in allBooksOfThatName:
            sum += particularBook.rating
        avgRating = sum/allBooksOfThatName.count()
        book.rating = avgRating
        book.save()

        return redirect('book-list')
