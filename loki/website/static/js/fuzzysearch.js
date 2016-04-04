(function () {
    $(document).ready(function () {

        $('.dateinput').datepicker({
            dateFormat: "yy",
            changeMonth: false,
            changeYear: true,
            showButtonPanel: true,
            onChangeMonthYear: function (year, mohth, inst) {
                $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
            },
            onClose: function (dateText, inst) {
                $(this).datepicker('setDate', new Date(inst.selectedYear, inst.selectedMonth, 1));
            }
        });

        if ($("#id_studies_at").length > 0) {

            // preset the data because of reasons
            $(".dateinput#id_start_date").attr("placeholder", "Учене от").val("");
            $(".dateinput#id_end_date").attr("placeholder", "Учене до").val("");

            var suggestion_dropdown = $("<div id='suggestion-dropdown'><ul></ul></div>");

            $("#id_studies_at").val("").after(suggestion_dropdown);
            var field = $("#id_studies_at").clone();
            field.attr("name", '');
            field.attr('id', 'fuzzy-field');
            $("#id_studies_at").hide().after(field);
            $("#id_education_info").hide();

            suggestion_dropdown = suggestion_dropdown.find("ul");

            var last_content = "";
            var requests_waiting = 0;
            var last_keyup = Date.now();
            window.timeout = false;

            $("#fuzzy-field").keyup(function (e) {

                if (fuzzysearch_navigation(e.which)) {
                    e.preventDefault();
                    return;
                }

                if (!timeout)
                    timeout = setTimeout(function () {

                        $("#suggestion-dropdown").show();

                        var value = $.trim($("#fuzzy-field").val());

                        if (value == "") {
                            $("#suggestion-dropdown").hide();
                            suggestion_dropdown.html("");
                            return;
                        }

                        if (value == last_content) return;
                        last_content = value;

                        requests_waiting++;
                        suggestion_dropdown.fadeTo("fast", 0.4);

                        $.ajax({
                            url: '/base/api/education-place-suggest/',
                            type: "POST",
                            data: {
                                query: value
                            },
                            success: function (data) {

                                requests_waiting--;
                                clearTimeout(timeout);
                                timeout = false;

                                if (requests_waiting == 0) {
                                    suggestion_dropdown.fadeTo("fast", 1);

                                    suggestion_dropdown.html("");

                                    for (var i in data['result']) {
                                        var el = data['result'][i];
                                        var str = represent(el);

                                        if (i == 0) {
                                            suggestion_dropdown.append($("<li class='selected' ref='" + el.pk + "'>" + str + "</li>"));
                                        } else {
                                            suggestion_dropdown.append($("<li ref='" + el.pk + "'>" + str + "</li>"));
                                        }
                                    }
                                    suggestion_dropdown.append($("<li rel='add_new'>" + "Не намирам моето" + "</li>"));
                                }
                            }
                        })
                    }, 1000);
            });

            $(".register-form").submit(function (e) {
                if ($(":focus").is($("#fuzzy-field"))) {
                    e.preventDefault();
                    return;
                }

                // Forgive me father, for I have sinned
                $("#id_start_date").val($("#id_start_date").val() + "-" + 1 + "-" + 1);
                $("#id_end_date").val($("#id_end_date").val() + "-" + 1 + "-" + 1);

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

    function represent(el) {
        var str = "";
        if (el.subject) {
            str += " " + el.subject;
        }

        if (el.faculty) {
            str += " " + el.faculty;
        }

        if (el.educationplace) {
            str += " " + el.educationplace;
        }

        if (el.city) {
            str += " " + el.city;
        }

        return str;
    }


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
        // if an item from suggestion is selected - fill the ed_info field
        var el = $("#suggestion-dropdown .selected")
        if (el.attr('ref')) {
            $("#id_education_info").val(el.attr('ref'));
            $("#fuzzy-field").val(el.html())
            $("#id_studies_at").val("");
            $("#suggestion-dropdown").hide();
        } else {
            // if the "other thing" option is selected from the dropdown - fill in the "studies at" field
            if (el.attr("rel")) {
                $("#id_education_info").val("")
                $("#id_studies_at").val($("#fuzzy-field").val());
                $("#suggestion-dropdown").hide();
            }
        }
    }

})();