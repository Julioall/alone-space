from PIL import Image

def process_spritesheet(filename, output_name, sprite_width, sprite_height):
    """
    Processa um spritesheet para recortar cada frame e salvá-lo como uma imagem individual.

    Args:
        filename (str): Caminho do arquivo do spritesheet.
        output_name (str): Prefixo para os arquivos de saída.
        sprite_width (int): Largura de cada sprite.
        sprite_height (int): Altura de cada sprite.

    Returns:
        None
    """
    try:
        # Carregar o spritesheet
        spritesheet = Image.open(filename)
        sheet_width, sheet_height = spritesheet.size
        print(f"Tamanho do spritesheet: {sheet_width}x{sheet_height}")

        # Calcular o número de colunas e linhas
        columns = sheet_width // sprite_width
        rows = sheet_height // sprite_height
        print(f"Número de colunas: {columns}, Número de linhas: {rows}")

        # Recortar e salvar cada frame
        frame_number = 1
        for row in range(rows):
            for col in range(columns):
                left = col * sprite_width
                top = row * sprite_height
                right = left + sprite_width
                bottom = top + sprite_height
                box = (left, top, right, bottom)
                frame = spritesheet.crop(box)

                # Salvar frame com nome sequencial
                frame.save(f"{output_name}-{frame_number}.png")
                print(f"Salvo: {output_name}-{frame_number}.png")
                frame_number += 1

        print("Processamento concluído!")

    except Exception as e:
        print(f"Erro ao processar o spritesheet: {e}")

# Usando a ferramenta
process_spritesheet("big-bullet.png", "big-bullet", 8, 16)
