import kotlin.math.exp
import kotlin.math.max
import kotlin.random.Random
/*
fun main1(args: Array<String>) {
    val string = readLine()!!
    val split = string.split(" ")
    var a = split[0].toInt()
    var b = split[1].toInt()
    var c = split[2].toInt()

    println("<$a>.<$b>.<$c>")
}

fun main2(args: Array<String>) {
    val string = readLine()!!
    val split = string.split(" ")
    var max = Double.MIN_VALUE
    var max2 = Double.MIN_VALUE
    for (s in split) {
        val digit = s.toDoubleOrNull()
        if (digit != null && max <= digit) {
            max2 = max
            max = digit
        } else if (digit != null && max2 < digit) {
            max2 = digit
        }
    }
    println(max + max2)
}

fun main3(args: Array<String>) {
    val string = readLine()!!
    val split = string.split(" ")
    var x = split[0].toDouble()
    var y = split[1].toDouble()
    var r = split[2].toDouble()

    if (x * x + y * y <= r * r)
        println("YES")
    else
        println("NO")
}

fun main4(args: Array<String>) {
    val string = readLine()!!
    val split = string.split(" ")
    var x = split[0].toDouble()
    var y = split[1].toDouble()
    var r = split[2].toDouble()
    var x0 = split[3].toDouble()
    var y0 = split[4].toDouble()

    if ((x - x0) * (x - x0) + (y - y0) * (y - y0) <= r * r)
        println("YES")
    else
        println("NO")
}

fun main_using_when(args: Array<String>) {
    val string = readLine()!!
    val digit = string.toDouble()
    val result = when {
        digit % 2 == 0.0 -> 2
        digit % 3 == 0.0 -> 3
        digit % 4 == 0.0 -> 4
        digit % 5 == 0.0 -> 5
        else -> -1
    }
    println(result)
}

fun main_using_until_and_downTo(args: Array<String>) {
    for (i in 0..10)
        print(i)

    for (i in 0 until 10)
        println(i)

    for (i in 10 downTo 0)
        println(i)
}

fun main_array(args: Array<String>) {
    val n = 1
    val a = Array(n) {index -> index}
    val b = arrayOf(" ", "S", "A", "V")
    val c = emptyArray<String>()

    val list = ArrayList<String>()
    list.add(" ")
    list.add("S")

    val list1 = listOf<String>(" ", "sas")
    val list2 = mutableListOf<String>(" ", "sas")
    list2.add("asa")

}

fun main_array_problem(args: Array<String>) {
    val array = Array(10) {
        Random.nextInt(0, 100)
    }
    var sum = 0
    for (int in array)
        sum += int
    println(sum)
}

fun main_array_problem1(args: Array<String>) {
    val string = readLine()!!
    val split = string.split(" ")
    var sum = 0
    for (i in 0 until split.size) {
        val el = split[i].toInt()
        println("$i $el")
        if ((i % 2 == 0) && el > 0)
            sum += el
    }
    println(sum)
}

fun problem_2_4(args: Array<String>) {
    var words = emptyArray<String>()
    var counts = emptyArray<Int>()
    val split = text.split(" ")
    for (i in 0 until split.size) {
        val word = split[i]
        if (words.contains(word)) {
            val index = words.indexOf(word)
            counts[index]++
        } else {
            words = words.plusElement(word)
            counts = counts.plusElement(1)
        }
    }
    for (i in 0 until words.size) {
        println("${words[i]} ${counts[i]}")
    }

}

val text = "Ñìåøàííûå ÷óâñòâà òåñíÿòñÿ â ãðóäè ìîåé, êîãäà ÿ ïðèñòóïàþ ê îïèñàíèþ ýòîé ýêñïåäèöèè, ïðèíåñøåé ìíå áîëüøå, íåæåëè ÿ ìîã íàäåÿòüñÿ. Îòïðàâëÿÿñü â ïóòü ñ Çåìëè, ÿ íàçíà÷èë ñåáå öåëüþ äîñòèæåíèå íåâåðîÿòíî äàëåêîé ïëàíåòû â ñîçâåçäèè Êðàáà, Çàçüÿâû, ñëàâà î êîòîðîé ðàçíîñèòñÿ ïî âñåé êîñìè÷åñêîé ïóñòîòå áëàãîäàðÿ òîìó, ÷òî îíà ïîäàðèëà Âñåëåííîé îäíó èç íàèáîëåå âûäàþùèõñÿ åå ëè÷íîñòåé, Ó÷èòåëÿ Îõ. Íå òàê íà ñàìîì äåëå çîâóò ñåãî áëåñòÿùåãî ìûñëèòåëÿ, ÿ æå ïîëüçóþñü ýòèì èìåíåì, èáî íè îäèí çåìíîé ÿçûê íå â ñîñòîÿíèè ïåðåäàòü åãî èíûì îáðàçîì. Ðåáåíêó, ðîæäàþùåìóñÿ íà Çàçüÿâå, âìåñòå ñ íåîáûêíîâåííî äëèííûì, ïî íàøèì ïðåäñòàâëåíèÿì, èìåíåì ïðèñâàèâàþò íåñìåòíîå ìíîæåñòâî òèòóëîâ è îòëè÷èé.\n" +
        "Êîãäà â ñâîå âðåìÿ Ó÷èòåëü Îõ ïðèøåë â ìèð, åãî íàðåêëè èìåíåì Ãðèäèïèäàãèòèòîñèòèïîïîêàðòóðòåãâàóàíà-òîïî÷òîýòîòàì. Îí ïîëó÷èë òèòóëû Çëàòîòêàíîãî Îïëîòà Áûòèÿ, Äîêòîðà Ñîâåðøåííîé Êðîòîñòè, Ñâåòëîé Âåðîÿòíîñòíîé Âñåñòîðîííîñòè è ò.ä. è ò.ï. Ïî ìåðå òîãî êàê îí ìóæàë è ó÷èëñÿ, êàæäûé ãîä åãî ëèøàëè îäíîãî òèòóëà è ÷àñòè÷êè èìåíè, à ïîñêîëüêó ñïîñîáíîñòè îí âûêàçûâàë íåîáû÷àéíûå, óæå íà òðèäöàòü òðåòüåì ãîäó æèçíè ó íåãî îòîáðàëè ïîñëåäíåå îòëè÷èå, ñïóñòÿ æå åùå äâà ãîäà ó íåãî âîîáùå íå îñòàëîñü òèòóëîâ, à èìÿ åãî îáîçíà÷àëîñü îäíîé òîëüêî  äà ê òîìó æå íåìîé  áóêâîé çàçüÿâñêîãî àëôàâèòà: «ïðèäûõàíèå áëàæåíñòâà», òî åñòü îñîáîãî ðîäà ïîäàâëåííûé âçäîõ, êîòîðûé èçäàþò îò èçáûòêà óâàæåíèÿ è íàñëàæäåíèÿ."

fun problem_3_1(args: Array<String>) {
    val a = readLine()!!
    var fl = 0
    for (i in 0 until a.length) {
        if (a[i] != a[a.length - i - 1]) {
            fl = 1
        }
    }
    if (fl == 0) {
        println("Yes")
    } else {
        println("No")
    }
}

fun problem_3_2(args: Array<String>) {
    val a = readLine()!!
    val b = readLine()!!.toInt()
    for (i in 0 until b) {
        for (j in 0 until (i + 1)) {
            print(a[j])
        }
        println()
    }
}

fun problem_3_3(args: Array<String>) {
    val a = readLine()!!.toLowerCase()
    var use = emptyArray<Char>()
    for (i in 0 until a.length) {
        if (a[i] == 'a' || a[i] == 'o' || a[i] == 'u' || a[i] == 'e' || a[i] == 'i') {
            if (!use.contains(a[i]))
                print("${a[i]} ")
            use = use.plusElement(a[i])
        }
    }
    println()
    for (i in 0 until a.length) {
        if (a[i] != 'a' && a[i] != 'o' && a[i] != 'u' && a[i] != 'e' && a[i] != 'i') {
            if (!use.contains(a[i]))
                print("${a[i]} ")
            use = use.plusElement(a[i])
        }
    }
}

fun problem_3_4(args: Array<String>) {
    val split = text.split(" ")
    var word = emptyArray<String>()
    for (i in 0 until split.size) {
        var fl = 0
        for (j in 0 until word.size) {
            if (split[i] == word[j])
                fl = 1
        }
        if (fl == 0)
            word = word.plusElement(split[i])
    }
    println(word.size)
}

fun problem_class(args: Array<String>) {
    val split = text.split(" ")
    var word = emptyArray<String>()
    for (i in 0 until split.size) {
        var fl = 0
        for (j in 0 until word.size) {
            if (split[i] == word[j])
                fl = 1
        }
        if (fl == 0)
            word = word.plusElement(split[i])
    }
    println(word.size)
}

/*fun main(args: Array<String>) {
    val character = Character("War", 1, 80, Unit, 20)
    character.gainExperience(200)
    println(character.level)

}*/



//open class User
//abstract class User
//class MultiplayerUser: User()

class User() {
    var a : Int = 1
    fun sas() {
        a++
    }
}


open class Character(
    private var name: String,
    private var hitpoints: Int,
    var level: Int,
    private var rightHand: Any,
    var experience: Int
) {
    private var lvltop = 100

    fun gainExperience(value: Int) {
        val exp = experience + value
        if (exp >= lvltop) {
            level++
            //
        }
        experience += value
    }

    fun getObjectInRightHand(`object`: Any) {
        rightHand = `object`
    }

}



*/


/*
class Player(
    private var name: String,
    private var _class:String,
    private var dex:Int = 1,
    private var str: Int = 1,
    private var lvl:Int = 1,
    private var maxHP:Int = 10,
    private var nextLvlXP: Int= 10,
    private var XP:Int = 0,
    private var HP:Int = 10
) {
    init {
        HP += attributeBonus()
    }
    fun askHP() : Int {
        return HP
    }


    fun lvlUp(){
        lvl+=1
        str += if (lvl % 2 == 0) 1 else 0
        dex += if (lvl % 2 == 1) 1 else 0
        maxHP = (maxHP*1.1).toInt()
        nextLvlXP *= 2
        HP = maxHP
        println ("Lvl up! Your stats are ${toString()}")
    }

    fun increaseXP(newXP : Int){
        println("Got ${newXP} XP")
        XP += newXP
        if (XP > nextLvlXP) lvlUp()
    }

    fun calcDmg(): Int {
        return str * lvl + dex
    }

    fun calcDodge(enemyDex: Int): Boolean {
        return (lvl * dex) > enemyDex
    }

    override fun toString(): String {
        return "Player(name=$name, lvl=$lvl, str=$str)"
    }

    fun attributeBonus(): Int {
        return str * lvl
    }
}


fun main(args: Array<String>){
    val player = Player("hero1", "warrior")
    //for (i in 0 until 5) player.increaseXP(5)
    println(player)
    println(player.attributeBonus())
    println(player.askHP())
}

open class Character(val name: String, val level: Int, val str: Int) {
    open fun getBonus() = level * str

    protected fun protectedFun() {
        //...

    }
}

class CharacterNPC(name: String, level: Int, str: Int, private val hp: Int): Character(name, level, str) {
    init {
        println(getBonus())
        protectedFun()
    }

    fun getAltBonus() = getBonus() * hp

}

fun CharacterNPC.printName(): String {
    return this.name
}*/



fun main(args: Array<String>){
    var split = readLine()!!
    var n = split.toInt()
    while (n > 0) {

    }
}

