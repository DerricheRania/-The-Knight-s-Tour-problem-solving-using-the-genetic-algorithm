import random
import pygame
import sys

class Chromosome:
    """Classe représentant un chromosome (séquence de mouvements)"""
    
    def __init__(self, genes=None):
        """Initialise un chromosome avec des gènes aléatoires ou donnés"""
        if genes is None:
            self.genes = [random.randint(1, 8) for _ in range(63)]
        else:
            self.genes = genes.copy()
    
    def crossover(self, partner):
        """Croisement à un point avec un autre chromosome"""
        crossover_point = random.randint(1, len(self.genes) - 1)
        child1_genes = self.genes[:crossover_point] + partner.genes[crossover_point:]
        child2_genes = partner.genes[:crossover_point] + self.genes[crossover_point:]
        return Chromosome(child1_genes), Chromosome(child2_genes)
    
    def mutation(self, mutation_rate=0.01): # teacher told us to use rate 0.01
        """Mutation aléatoire des gènes"""
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = random.randint(1, 8)


class Knight:
    """Classe représentant un cavalier sur l'échiquier"""
    
    MOVES = {

         1: (1, 2),   # 2 up 1 right
         2: (-1, 2),  # 2 up 1 left
         3: (1, -2),    # 2 down 1 right
         4: (-1, -2),   # 2 down 1 left
         5: (-2, 1),  # 2 left 1 up
         6: (-2, -1),   # 2 left 1 down
         7: (2, 1),   # 2 right 1 up
         8: (2, -1)     # 2 right 1 down
    }
    
    def __init__(self, chromosome=None):
        """Initialise un cavalier avec un chromosome"""
        if chromosome is None:
            self.chromosome = Chromosome()
        else:
            self.chromosome = chromosome
        
        self.position = (0, 0) # start at (0,0)
        self.fitness = 0 # number of squares visited
        self.path = [(0, 0)] # list of visited squares
    
    def move_forward(self, direction):
        """Déplace le cavalier dans une direction donnée"""
        dx, dy = self.MOVES[direction]
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        self.position = (new_x, new_y)
        return self.position
    
    def move_backward(self, direction):
        """Annule un mouvement (retour en arrière)"""
        dx, dy = self.MOVES[direction]
        new_x = self.position[0] - dx
        new_y = self.position[1] - dy
        self.position = (new_x, new_y)
        return self.position
    
    def is_valid_position(self, pos):
        """Vérifie si une position est valide (sur l'échiquier et non visitée)"""
        x, y = pos
        return (0 <= x < 8 and 0 <= y < 8 and pos not in self.path)
    
    def check_moves(self):
        """Vérifie et corrige les mouvements invalides"""
        self.position = (0, 0)
        self.path = [(0, 0)]
        cycle_forward = random.choice([True, False])
        
        for gene in self.chromosome.genes:
            move = gene
            valid_move_found = False
            test_pos = (self.position[0] + self.MOVES[move][0], 
                       self.position[1] + self.MOVES[move][1])
            
            if self.is_valid_position(test_pos):
                self.move_forward(move)
                self.path.append(self.position)
                valid_move_found = True
            else:
                current_move = move
                for _ in range(7):
                    if cycle_forward:
                        current_move = (current_move % 8) + 1
                    else:
                        current_move = ((current_move - 2) % 8) + 1
                    
                    test_pos = (self.position[0] + self.MOVES[current_move][0],
                               self.position[1] + self.MOVES[current_move][1])
                    
                    if self.is_valid_position(test_pos):
                        self.move_forward(current_move)
                        self.path.append(self.position)
                        valid_move_found = True
                        break
                
                if not valid_move_found:
                    break
    # Purpose = ensure knight does not leave the board and does not revisit squares.
    def evaluate_fitness(self):
        """Évalue la fitness du cavalier (nombre de cases visitées)"""
        self.check_moves()
        self.fitness = len(self.path)
        return self.fitness


class Population:
    """Classe représentant une population de cavaliers"""
    
    def __init__(self, population_size):
        """Initialise une population de cavaliers"""
        self.population_size = population_size
        self.generation = 1 # number of generations
        self.knights = [Knight() for _ in range(population_size)] # list of Knight objects
    
    def check_population(self):
        """Vérifie la validité des mouvements de tous les cavaliers"""
        for knight in self.knights:
            knight.check_moves()
    
    def evaluate(self):
        """Évalue tous les cavaliers et retourne le meilleur"""
        best_knight = None
        max_fitness = 0
        
        for knight in self.knights:
            fitness = knight.evaluate_fitness()
            if fitness > max_fitness:
                max_fitness = fitness
                best_knight = knight
        
        return max_fitness, best_knight
    
    def tournament_selection(self, size=3):
        """Sélection par tournoi pred 3 knights ystfhom par fitness and takes the best 2"""
        tournament = random.sample(self.knights, size)
        tournament.sort(key=lambda k: k.fitness, reverse=True)
        return tournament[0], tournament[1] # best 2
    
    def create_new_generation(self):
        """Crée une nouvelle génération"""
        new_knights = []
        
        while len(new_knights) < self.population_size:
            parent1, parent2 = self.tournament_selection(3)
            child1_chromo, child2_chromo = parent1.chromosome.crossover(parent2.chromosome)
            child1_chromo.mutation()
            child2_chromo.mutation()
            new_knights.append(Knight(child1_chromo))
            if len(new_knights) < self.population_size:
                new_knights.append(Knight(child2_chromo))
        
        self.knights = new_knights
        self.generation += 1


class KnightTourAnimation:
    """Classe pour l'animation Pygame du parcours du cavalier"""
    
    def __init__(self, knight):
        """Initialise l'animation avec la solution trouvée"""
        pygame.init()
        
        # Paramètres de la fenêtre
        self.SQUARE_SIZE = 80
        self.BOARD_SIZE = 8
        self.WINDOW_SIZE = self.SQUARE_SIZE * self.BOARD_SIZE
        self.INFO_HEIGHT = 100
        
        # Couleurs
        self.COLOR_LIGHT = (240, 217, 181)  # Beige clair
        self.COLOR_DARK = (181, 136, 99)    # Marron
        self.COLOR_KNIGHT = (255, 0, 0)     # Rouge pour le cavalier
        self.COLOR_PATH = (0, 100, 255)     # Bleu pour le chemin
        self.COLOR_VISITED = (100, 255, 100) # Vert pour cases visitées
        self.COLOR_TEXT = (0, 0, 0)         # Noir
        self.COLOR_BG = (50, 50, 50)        # Gris foncé
        
        # Création de la fenêtre
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE + self.INFO_HEIGHT))
        pygame.display.set_caption("Knight's Tour - Animation de la Solution")
        
        # Police
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Données du cavalier
        self.knight = knight
        self.path = knight.path
        self.current_step = 0
        self.animation_speed = 500  # millisecondes entre chaque mouvement
        self.last_update = pygame.time.get_ticks()
        self.paused = False

        self.knight_img = pygame.image.load("Knight.png")
        self.knight_img = pygame.transform.scale(self.knight_img, (60, 60))

        
    def draw_board(self):
        """Dessine l'échiquier"""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                color = self.COLOR_LIGHT if (row + col) % 2 == 0 else self.COLOR_DARK
                pygame.draw.rect(self.screen, color,
                               (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                self.SQUARE_SIZE, self.SQUARE_SIZE))
    
    def draw_visited_squares(self):
        """Dessine les cases déjà visitées"""
        for i in range(self.current_step + 1):
            x, y = self.path[i]
            # Overlay semi-transparent vert
            s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(self.COLOR_VISITED)
            self.screen.blit(s, (x * self.SQUARE_SIZE, y * self.SQUARE_SIZE))
            
            # Numéro de la visite
            text = self.small_font.render(str(i + 1), True, self.COLOR_TEXT)
            text_rect = text.get_rect(center=(x * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                              y * self.SQUARE_SIZE + self.SQUARE_SIZE // 2))
            self.screen.blit(text, text_rect)
    
    def draw_path(self):
        """Dessine le chemin parcouru"""
        if self.current_step > 0:
            for i in range(self.current_step):
                x1, y1 = self.path[i]
                x2, y2 = self.path[i + 1]
                
                start_pos = (x1 * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                           y1 * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                end_pos = (x2 * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                          y2 * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
                
                pygame.draw.line(self.screen, self.COLOR_PATH, start_pos, end_pos, 3)
    
    def draw_knight(self):
      """Dessine le cavalier avec une vraie image PNG"""
      if self.current_step < len(self.path):
        x, y = self.path[self.current_step]

        # Compute position
        pos_x = x * self.SQUARE_SIZE + (self.SQUARE_SIZE - 60)//2
        pos_y = y * self.SQUARE_SIZE + (self.SQUARE_SIZE - 60)//2

        # Draw the knight image
        self.screen.blit(self.knight_img, (pos_x, pos_y))
    
    def draw_info(self):
        """Dessine les informations en bas de l'écran"""
        info_y = self.WINDOW_SIZE
        pygame.draw.rect(self.screen, self.COLOR_BG, 
                        (0, info_y, self.WINDOW_SIZE, self.INFO_HEIGHT))
        
        # Informations
        step_text = f"Étape: {self.current_step + 1}/{len(self.path)}"
        fitness_text = f"Fitness: {self.knight.fitness}/64"
        status_text = "PAUSE" if self.paused else "EN COURS"
        
        # Affichage
        step_surface = self.font.render(step_text, True, (255, 255, 255))
        fitness_surface = self.font.render(fitness_text, True, (255, 255, 255))
        status_surface = self.font.render(status_text, True, (255, 255, 0) if self.paused else (0, 255, 0))
        
        self.screen.blit(step_surface, (20, info_y + 20))
        self.screen.blit(fitness_surface, (20, info_y + 55))
        self.screen.blit(status_surface, (self.WINDOW_SIZE - 200, info_y + 35))
        
        # Instructions
        instructions = self.small_font.render("ESPACE: Pause/Play | +/-: Vitesse | R: Recommencer | Q: Quitter", 
                                              True, (200, 200, 200))
        self.screen.blit(instructions, (20, info_y + 85))
    
    def update(self):
        """Met à jour l'animation"""
        current_time = pygame.time.get_ticks()
        
        if not self.paused and current_time - self.last_update > self.animation_speed:
            if self.current_step < len(self.path) - 1:
                self.current_step += 1
                self.last_update = current_time
            else:
                # Animation terminée
                self.paused = True
    
    def reset(self):
        """Redémarre l'animation"""
        self.current_step = 0
        self.paused = False
        self.last_update = pygame.time.get_ticks()
    
    def run(self):
        """Boucle principale de l'animation"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.animation_speed = max(50, self.animation_speed - 50)
                    elif event.key == pygame.K_MINUS:
                        self.animation_speed = min(2000, self.animation_speed + 50)
            
            # Mise à jour
            self.update()
            
            # Dessin
            self.draw_board()
            self.draw_visited_squares()
            self.draw_path()
            self.draw_knight()
            self.draw_info()
            
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        pygame.quit()


def main():
    """Fonction principale exécutant l'algorithme génétique"""
    population_size = 50
    
    # Créer la population initiale
    population = Population(population_size)
    
    print("Démarrage de l'algorithme génétique...")
    print(f"Taille de la population: {population_size}")
    print("-" * 50)
    
    while True:
        # Vérifier la validité de la population actuelle
        population.check_population()
        
        # Évaluer la génération actuelle
        max_fit, best_solution = population.evaluate()
        
        print(f"Génération {population.generation}: Meilleure fitness = {max_fit}/64")
        
        # Condition d'arrêt
        if max_fit == 64:
            print("\n✓ Solution optimale trouvée!")
            print(f"Nombre de générations: {population.generation}")
            break
        
        # Limite de sécurité pour éviter une boucle infinie
        if population.generation >= 100000:
            print("\nLimite de générations atteinte (100000)")
            print(f"Meilleure solution trouvée: {max_fit}/64")
            break
        
        # Générer la nouvelle population
        population.create_new_generation()
    
    # Lancer l'animation Pygame
    print("\nLancement de l'animation...")
    animation = KnightTourAnimation(best_solution)
    animation.run()
    
    return best_solution


if __name__ == "__main__":
    main()