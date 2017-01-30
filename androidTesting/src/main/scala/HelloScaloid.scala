package androidtesting

import android.graphics.Color
import org.scaloid.common._

class HelloScaloid extends SActivity {
  lazy val meToo = new STextView("Me too")
  lazy val redBtn = new SButton(R.string.red)
  lazy val buttonTwo = new SButton(R.string.red).textColor(Color.YELLOW)

  onCreate {
    contentView = new SVerticalLayout {
      style {
        case b: SButton => b.textColor(Color.RED).onClick(meToo.text = "PRESSED")
        case t: STextView => t textSize 10.dip
        case e: SEditText => e.backgroundColor(Color.YELLOW).textColor(Color.BLACK)
      }
      STextView("I am 10 dip tall")
      meToo.here
      STextView("I am 15 dip tall") textSize 15.dip // overriding
      new SLinearLayout {
        STextView("Button: ")
        redBtn.here
      }.wrap.here
      new SLinearLayout {
        STextView("Another: ")
        buttonTwo.here
      }.wrap.here
      SButton("Can I use a string?") onClick(meToo.text = "Other Press")
      SEditText("Yellow input field fills the space").fill
    } padding 20.dip
  }

}
