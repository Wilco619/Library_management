$(document).ready(function() {
    $('#book-search').on('keyup', function() {
        var searchTerm = $(this).val();
        if (searchTerm.length >= 3) {
            $.ajax({
                type: 'POST',
                url: '{% url "search_book" %}',
                data: {
                    'book_search': searchTerm,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                success: function(data) {
                    $('#search-results').html(data);
                }
            });
        } else {
            $('#search-results').empty();
        }
    });
});
