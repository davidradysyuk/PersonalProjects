import java.util.Scanner;
import java.io.IOException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.util.List;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        List<String> validTeams = List.of("ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NYK","NO", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTAH", "WAS");

        while (true) {
            System.out.print("Enter the first NBA team abbreviation, or type TEAMS to show a list (or 'quit' to exit): ");
            String team1 = scanner.nextLine().toUpperCase();

            if (team1.equals("QUIT")) {
                break;
            }
            if (team1.equals("TEAMS")) {
                System.out.println(validTeams);
                continue;
            }
            if (!validTeams.contains(team1)) {
                System.out.println("Invalid team abbreviation. Please enter a valid abbreviation.");
                continue;
            }

            System.out.print("Enter the second NBA team abbreviation: ");
            String team2 = scanner.nextLine().toUpperCase();

            if (!validTeams.contains(team2)) {
                System.out.println("Invalid team abbreviation. Please enter a valid abbreviation.");
                continue;
            }

            try {
                double[] team1Scores = processTeam(team1);
                double[] team2Scores = processTeam(team2);

                double newTeam1OffensiveScore = team1Scores[0] - team2Scores[1];
                double newTeam2OffensiveScore = team2Scores[0] - team1Scores[1];

                System.out.println("Offensive Score for " + team1 + ": " + newTeam1OffensiveScore);
                System.out.println("Offensive Score for " + team2 + ": " + newTeam2OffensiveScore);

                calculateWinningChance(team1, team2, newTeam1OffensiveScore, newTeam2OffensiveScore);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public static double[] processTeam(String team) throws IOException {
        double[] scores = new double[2]; // Index 0: Offensive Score, Index 1: Defensive Score

        Document doc = Jsoup.connect("https://www.espn.com/nba/team/stats/_/name/"+team).timeout(6000).get();
        Element tableScroller = doc.getElementsByClass("Table__Scroller").first();

        if (tableScroller != null) {
            Elements trElements = tableScroller.select("tr");

            // Iterate over players in reverse order
            for (int i = trElements.size() - 1; i >= 0; i--) {
                Element trElement = trElements.get(i);
                Elements tdElements = trElement.select("td");

                if (tdElements.size() >= 13) {
                    Elements spanElement = tdElements.select("td");

                    if (spanElement != null) {
                        String digit = spanElement.text();
                        String[] digitsArray = digit.split("\\s+");

                        if (digitsArray.length >= 8) {
                            double offensiveScore = Double.parseDouble(digitsArray[1]) + Double.parseDouble(digitsArray[2]) + Double.parseDouble(digitsArray[4]);
                            double defensiveScore = Double.parseDouble(digitsArray[3]) + Double.parseDouble(digitsArray[6]) + Double.parseDouble(digitsArray[7]);

                            scores[0] = offensiveScore;
                            scores[1] = defensiveScore;

                            System.out.println("Team: " + team);
                            break; // Stop after processing the team
                        }
                    }
                }
            }
        }

        return scores;
    }
    public static void calculateWinningChance(String team1, String team2, double newTeam1OffensiveScore, double newTeam2OffensiveScore) {
        double scoreDifference = Math.abs(newTeam1OffensiveScore - newTeam2OffensiveScore);
        double winningChance;

        if (newTeam1OffensiveScore > newTeam2OffensiveScore) {
            winningChance = 50 + (scoreDifference * 1.5);
            System.out.println(team1 + " has a " + winningChance + "% chance of winning.");
        } else if (newTeam2OffensiveScore > newTeam1OffensiveScore) {
            winningChance = 50 + (scoreDifference * 1.5);
            System.out.println(team2 + " has a " + winningChance + "% chance of winning.");
        } else {
            System.out.println("It's an even match!");
        }
    }
}

