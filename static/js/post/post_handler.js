    $(document).ready(function(){

        $('#id_type_automobile').hide()
        $('#id_type_immobilier').hide()
        $('label[for=id_type_automobile').hide()
        $('label[for=id_type_immobilier').hide()

          $("#id_category").change(function(){

            var value = $(this).val();

            if (value === 'Immobilier')
            {
                $('#id_type_immobilier').show()
                 $('label[for=id_type_immobilier').show()

                $('#id_type_automobile').hide()
                 $('label[for=id_type_automobile').hide()
            }
            else if (value ==='Automobile')
            {
                $('#id_type_automobile').show()
                 $('label[for=id_type_automobile').show()

                 $('#id_type_immobilier').hide()
                 $('label[for=id_type_immobilier').hide()
            }

            else {
                $('#id_type_automobile').hide()
                $('#id_type_immobilier').hide()

                  $('label[for=id_type_automobile').hide()
                  $('label[for=id_type_immobilier').hide()
            }
        });
    })




