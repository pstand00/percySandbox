library(shiny)
library(dplyr)
library(rhandsontable)


( DF <- data.frame(Value = 1:10, Status = TRUE, Name = LETTERS[1:10],
                   Date = seq(from = Sys.Date(), by = "days", length.out = 10),
                   stringsAsFactors = FALSE) )


scA = c(
  'Upper Section',
  'Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes',
  'Total Score', 'Bonus', 'Total (Upper)',
  'Lower Section',
  '3 of A kind', '4 of A Kind', 'Full House',
  'Small Straight (4 in a row)', 'Large Straight (5 in a row)',
  'Yahtzee', 'Chance', 'Yahtzee Bonus',
  'Total of Lower Section', 'Total of Upper Section', 'Grand Total'
  ) %>% as.data.frame() %>% setNames('A') 

scB = c(
  'ZZUpper Section',
  'Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes',
  'Total Score', 'Bonus', 'Total (Upper)',
  'Lower Section',
  '3 of A kind', '4 of A Kind', 'Full House',
  'Small Straight (4 in a row)', 'Large Straight (5 in a row)',
  'Yahtzee', 'Chance', 'Yahtzee Bonus',
  'Total of Lower Section', 'Total of Upper Section', 'Grand Total'
) %>% as.data.frame() %>% setNames('B')

dfA = matrix(
  c(
    'Upper Section',
    'Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes',
    'Total Score', 'Bonus', 'Total (Upper)',
    'Lower Section' ,
    '3 of A kind', '4 of A Kind', 'Full House',
    'Small Straight (4 in a row)', 'Large Straight (5 in a row)',
    'Yahtzee', 'Chance', 'Yahtzee Bonus',
    'Total of Lower Section', 'Total of Upper Section', 'Grand Total',
    # second 22
    'How To Score',
    'Count and Add Only Aces', 'Count and Add Only Twos',
    'Count and Add Only Threes', 'Count and Add Only Fours',
    'Count and Add Only Fives', 'Count and Add Only Sixes',
    '=', 'Score 35',
    '=', NA,
    'Add Total of All Dice', 'Add Total of All Dice', 
    'Score 25', 'Score 30', 
    'Score 40', 'Score 50', 
    'Score Total of All Dice', '100 times each Yahtzee',
    '=', '=',
    '='
  ), nrow = 22, ncol = 2
) %>% as.data.frame() %>% 
  setNames(c('Rolls', 'How To Score')) %>% 
         mutate(`Player 1` = NA, `Player 2` = NA, `Player 3` = NA, `Player 4` = NA) %>% 
  mutate(`Player 1` = as.numeric(`Player 1`),
         `Player 2` = as.numeric(`Player 2`),
         `Player 3` = as.numeric(`Player 3`),
         `Player 4` = as.numeric(`Player 4`))

rbind(scA, scB[, names(scA)])


editTable <- function(DF, outdir=getwd(), outfilename="table"){
  ui <- shinyUI(fluidPage(
    
    titlePanel("Edit and save a table"),
    sidebarLayout(
      sidebarPanel(
        helpText("Shiny app based on an example given in the rhandsontable package.", 
                 "Right-click on the table to delete/insert rows.", 
                 "Double-click on a cell to edit"),
        
        wellPanel(
          h3("Table options"),
          radioButtons("useType", "Use Data Types", c("TRUE", "FALSE"))
        ),
        br(), 
        
        wellPanel(
          h3("Save"), 
          actionButton("save", "Save table")
        )        
        
      ),
      
      mainPanel(
        
        rHandsontableOutput("hot")
        
      )
    )
  ))
  
  server <- shinyServer(function(input, output) {
    
    values <- reactiveValues()
    
    ## Handsontable
    observe({
      if (!is.null(input$hot)) {
        DF = hot_to_r(input$hot)
      } else {
        if (is.null(values[["DF"]]))
          DF <- DF
        else
          DF <- values[["DF"]]
      }
      values[["DF"]] <- DF
    })
    
    output$hot <- renderRHandsontable({
      DF <- values[["DF"]]
      if (!is.null(DF))
        rhandsontable(DF, useTypes = as.logical(input$useType), stretchH = "all")
    })
    
    ## Save 
    observeEvent(input$save, {
      finalDF <- isolate(values[["DF"]])
      saveRDS(finalDF, file=file.path(outdir, sprintf("%s.rds", outfilename)))
    })
    
  })
  
  ## run app 
  runApp(list(ui=ui, server=server))
  return(invisible())
}



editTable(dfA)
