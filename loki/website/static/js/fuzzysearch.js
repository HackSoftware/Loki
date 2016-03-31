(function () {
    $(document).ready(function () {

        if ($("#id_studies_at").length > 0) {

            var suggestion_dropdown = $("<div id='suggestion-dropdown'><ul></ul></div>");

            $("#id_studies_at").val("").after(suggestion_dropdown);
            var field = $("#id_studies_at").clone();
            field.attr("name", '');
            field.attr('id', 'fuzzy-field');
            $("#id_studies_at").hide().after(field);

            suggestion_dropdown = suggestion_dropdown.find("ul");

            var last_content = "";

            $("#fuzzy-field").keyup(function (e) {

                if (fuzzysearch_navigation(e.which)) {
                    e.preventDefault();
                    return;
                }

                $("#suggestion-dropdown").show();

                var value = $.trim($("#fuzzy-field").val());

                if (value == "") {
                    $("#suggestion-dropdown").hide();
                    suggestion_dropdown.html("");
                    return;
                }

                if (value == last_content) return;
                last_content = value;

                $.ajax({
                    url: '/base/api/education-place-suggest/',
                    type: "POST",
                    data: {
                        query: value
                    },
                    success: function (data) {

                        suggestion_dropdown.html("");

                        for (var i in data['result']) {
                            var el = data['result'][i];
                            var str = el.city + " " + el.uni + " " + el.faculty + " " + el.subject;

                            if (i == 0) {
                                suggestion_dropdown.append($("<li class='selected' ref='" + el.pk + "'>" + str + "</li>"));
                            } else {
                                suggestion_dropdown.append($("<li ref='" + el.pk + "'>" + str + "</li>"));
                            }
                        }
                    }
                })
            });

            $(".register-form").submit(function (e) {
                if ($(":focus").is($("#fuzzy-field"))) {
                    e.preventDefault();
                }
            }).on("mouseover", "#suggestion-dropdown li", function () {
                $("#suggestion-dropdown .selected").removeClass("selected");
                $(this).addClass("selected")
            }).on("click", "#suggestion-dropdown li", function () {
                select_item();
            });

            $(document).click(function (e) {
                if (!$(e.target).is("#suggestion-dropdown")) {
                    $("#suggestion-dropdown").hide();
                }
            })
        }
    });


    function fuzzysearch_navigation(keycode) {
        var el = $("#suggestion-dropdown .selected")
        if (keycode == 38) { // up
            if (el.prev().length > 0) {
                el.prev().addClass("selected")
                el.removeClass("selected")
            }
            return true;
        }

        if (keycode == 40) { // down
            if (el.next().length > 0) {
                el.next().addClass("selected");
                el.removeClass("selected");
            }
            return true;
        }

        if (keycode == 13) {
            select_item();
            return true;
        }

        return false;
    }

    function select_item() {
        var el = $("#suggestion-dropdown .selected")
        console.log(el)
        $("#id_studies_at").val(el.attr('ref'));
        $("#fuzzy-field").val(el.html())
        $("#suggestion-dropdown").hide();
    }

})();