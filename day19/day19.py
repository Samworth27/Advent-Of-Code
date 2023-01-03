from util.classes import Resource
from util.functions import read_file, prepare_state, affordable,debug_finish_build, debug_gather, debug_start_build





def best_path(blueprint,state, next_build = None):
    if next_build:
        # skip time until you can afford the next build or the end is reached
        
        while True:
            if state.step >= state.max_step:break
            if affordable(state.inventory, blueprint.costs[next_build]):break
            state.gather_resources()
            state.step += 1
            state.path.append(None)
        
        
        if state.step >= state.max_step:
            # if state.inventory.geode > state.best:
            #     print(F"Robots: {state.robots}\nInventory:{state.inventory}\nPath{state.path}\n")
            return state.inventory.geode

        
        state.start_build(next_build, blueprint.costs)
        # debug_start_build(next_build, blueprint.costs)
        state.gather_resources()
        # debug_gather(state)
        state.finish_build()
        state.path.append(next_build)
        # debug_finish_build(state,next_build)
        state.step += 1
        
    
    
    
    best = state.best
    if state.hypothetical_best() < best:
        return 0
    # determine choices
    for robot_type in state.build_options(blueprint.max_costs):
        new_state = state.copy()
        new_state.best = best
        best = max(best,best_path(blueprint, new_state, robot_type))
    
    return best
    
def main():
    
    blueprints = read_file()
    
    # Part 1
    # quality_levels = []
    # for blueprint in blueprints.values():
    #     best_count = best_path(blueprint,prepare_state(blueprint,24))
    #     quality_level = blueprint.id * best_count
    #     print(f"Blueprint {blueprint.id} has a count of {best_count} and a quality of {quality_level}")
    #     quality_levels.append(quality_level)
        
    # print(f"Sum of all quality levels is {sum(quality_levels)}")


    counts = []
    for blueprint in list(blueprints.values())[:3]:
        counts.append(best_path(blueprint,prepare_state(blueprint,32)))
        print(counts[-1])
    print(counts[0]*counts[1]*counts[2])


if __name__ == '__main__':
    main()
