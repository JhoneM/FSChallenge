$(document).ready(function () {

    $('#dataTables-user').DataTable({
        responsive: true
    });

    $('#dataTables-coin').DataTable({
        responsive: true
    });

    $('#dataTables-transactions').DataTable({
        responsive: true
    });

    $('#dataTables-account').DataTable({
        responsive: true
    });

    $('#dataTables-operations').DataTable({
        responsive: true
    });



    // ---------------------------- USUARIOS --------------------------------------------

    function deactivate_user(userId, username, activate) {

        $.ajax({
            data: {
                user_id: userId,
                username: username,
                activate: activate
            },
            type: "POST",
            url: "/users/deactivate"
        })
            .done(function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.sucessul);
                    location.reload();
                }
            });

    }

    $("#dataTables-user").on('click', '#editUserBtn', function (event) {
        event.preventDefault();
        $("#userIdEditPop").val("")
        $("#usernameEdit").val("")
        $("#nameEdit").val("")
        $("#lastnameEdit").val("")

        var currentRow = $(this).closest("tr");
        var userId = currentRow.find(".idUserBtn").val()
        var username = currentRow.find(".nameUserBtn").val()
        $("#userIdEditPop").val(userId)
        $("#usernameEdit").val(username)

    });

    $("#dataTables-user").on('click', '#descUserBtn', function (event) {
        event.preventDefault();
        var currentRow = $(this).closest("tr");
        var username = currentRow.find(".nameUserBtn").val()
        var userId = currentRow.find(".idUserBtn").val()
        var activate = 0
        deactivate_user(userId, username, activate)

    });

    $("#dataTables-user").on('click', '#actUserBtn', function (event) {
        event.preventDefault();
        var currentRow = $(this).closest("tr");
        var username = currentRow.find(".nameUserBtn").val()
        var userId = currentRow.find(".idUserBtn").val()
        var activate = 1
        deactivate_user(userId, username, activate)

    });

    $("#UpdateUser").click(function (event) {
        event.preventDefault();

        $.ajax({
            data: {
                username: $("#usernameEdit").val(),
                user_name: $("#nameEdit").val(),
                last_name: $("#lastnameEdit").val(),
                user_id: $("#userIdEditPop").val()
            },
            type: "POST",
            url: "/users/update"
        })
            .done(function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.sucessul);
                    location.reload();
                }
            });
    });

    $("#registerUser").submit(function (event) {
        var username = $(this).find("input[name=username]").val()
        var name = $(this).find("input[name=name]").val()
        var last_name = $(this).find("input[name=last_name]").val()
        var password = $(this).find("input[name=password]").val()
        var re_password = $(this).find("input[name=re_password]").val()
        var level = $(this).find("select[name=level]").val()

        $.ajax({
            data: {
                username: username,
                user_name: name,
                last_name: last_name,
                password: password,
                re_password: re_password,
                level: level,
            },
            type: "POST",
            url: "/users/register"
        })
            .done(function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.sucessul);
                    location.reload();
                }
            });

        event.preventDefault();
        return false;
    });


    // ---------------------------------------------------------------------------------------


    // --------------------------------------- MONEDAS ----------------------------------------------

    function deactivate_coin(coinId, coinName, activate) {

        $.ajax({
            data: {
                coinId: coinId,
                coinName: coinName,
                activate: activate
            },
            type: "POST",
            url: "/coins/deactivate"
        })
            .done(function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.sucessul);
                    location.reload();
                }
            });

    }

    $("#dataTables-coin").on('click', '#editCoinBtn', function (event) {
        event.preventDefault();
        $("#coinIdPop").val("")
        $("#coinNameEdit").val("")
        $("#isoEdit").val("")

        var currentRow = $(this).closest("tr");
        var coinId = currentRow.find("#idcoinBtn").val()
        var coinName = currentRow.find("td:eq(0)").text()
        var coinIso = currentRow.find("td:eq(1)").text();

        $("#coinIdPop").val(coinId)
        $("#coinNameEdit").val(coinName)
        $("#isoEdit").val(coinIso)

    });

    $("#UpdateCoin").click(function (event) {
        event.preventDefault();

        $.ajax({
            data: {

                coinId: $("#coinIdPop").val(),
                coinName: $("#coinNameEdit").val(),
                coinIso: $("#isoEdit").val(),
            },
            type: "POST",
            url: "/coins/update"
        })
            .done(function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.sucessful);
                    location.reload();
                }
            });
    });

    $("#registerCoin").submit(function (event) {
        var name = $(this).find("input[name=name]").val()
        var isoCode = $(this).find("input[name=iso]").val()

        $.ajax({
            data: {
                coinName: name,
                isoCode: isoCode,
            },
            type: "POST",
            url: "/coins/register"
        })
            .done(function (data) {
                if (data.error) {
                    alert(data.error)
                } else {
                    alert(data.sucessul);
                    location.reload();
                }
            });

        event.preventDefault();
        return false;
    });

    $("#dataTables-coin").on('click', '#descCoinBtn', function (event) {
        event.preventDefault();
        var currentRow = $(this).closest("tr");
        var coinId = currentRow.find("#idcoinBtn").val()
        var coinName = currentRow.find("td:eq(0)").text()
        var activate = 0
        deactivate_coin(coinId, coinName, activate)

    });

    $("#dataTables-coin").on('click', '#actCoinBtn', function (event) {
        event.preventDefault();
        var currentRow = $(this).closest("tr");
        var coinId = currentRow.find("#idcoinBtn").val()
        var coinName = currentRow.find("td:eq(0)").text()
        var activate = 1
        deactivate_coin(coinId, coinName, activate)

    });

    // ---------------------------------------------------------------------------------------

});