$(document).ready(function () {
    $("#lesson-continue-state").prop("disabled", true);
    const diceInput = $("#dice-input");
    diceInput.val('');
    diceInput.on('input', function () {
        if ($(this).val() === "") {
            $(this)[0].setCustomValidity("Bitte gib 5 Zahlen von 1-6 ein");
        } else {
            $(this)[0].setCustomValidity('');
        }
        const val = $(this).val();
        setDice(val)
    });
    $("#button-next").click(function () {
        if (diceInput.val() === "") {
            // TODO: remove
            diceInput.val("12345");
            diceInput[0].setCustomValidity('')
//            diceInput[0].setCustomValidity("Bitte gib 5 Zahlen von 1-6 ein");
        }
        if (!diceInput[0].checkValidity())
            return;
        const input = diceInput.val();
        findWord(input)

    });
});

let result = "";
let rounds = 1;

findWord = function (key) {
    const word = getDiceword(key).toUpperCase();
    result += " " + word;
    rounds++;
    $("#round-text").text("Runde " + rounds);
    $("#password-sentence").append(" " + word);
    $("#dice-input").val('');
    setDice("");
    if (rounds >= 7) {
        $("#topCont").hide();
        $("#bottomCont").hide();
        $("#introCont").hide();
        $("#resultCont").show();
        $("#passwordResult").append(result);
        $("#lesson-continue-state").prop("disabled", false);
    }
};

setDice = function (str) {
    for (let i = 1; i < 6; ++i) {
        const d = parseInt(str.charAt(i - 1), 10);
        if (!isNaN(d) || (d > 0 && d < 7)) {
            const dh = $("#dice-holder-" + i);
            dh.empty();
            dh.prepend($("#dice-" + d).clone());
            dh.children().show()
        } else {
            if (i == 1) {
                $("#dice-holder-" + i).children().css("visibility", "hidden")
            } else {
                $("#dice-holder-" + i).empty();
            }
        }
    }
};
