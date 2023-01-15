function watch(primary_key = "") {
    var data = {"pk": primary_key}
    $.ajax({
        type: 'GET',
        url: "/watch",
        data: data,
        dataType: 'text'
    })
}